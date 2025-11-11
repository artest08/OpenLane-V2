import os
from pathlib import Path

root_path = '/media/hdd/ek21/olv2_merged_100'
# Root contains: full_json_100, merged_100, test, train, val
# We want to create merged_100 with all scenarios from train, val, test
# For each scenario: image, lidar, sdmap.json from train/val/test
# info folder from full_json_100/train (or val/test)


def create_symbolic_links():
    # Source directories for image, lidar, sdmap
    train_orig = Path(os.path.join(root_path, "train"))
    val_orig = Path(os.path.join(root_path, "val"))
    test_orig = Path(os.path.join(root_path, "test"))
    
    # Source directory for info folders
    info_base = Path(os.path.join(root_path, "full_json_100"))
    
    # Target directory
    merged_folder = Path(os.path.join(root_path, "merged_100"))
    merged_folder.mkdir(exist_ok=True)
    
    # Check if source directories exist
    if not train_orig.exists() or not val_orig.exists() or not test_orig.exists():
        print(f"Error: One of the source directories does not exist")
        return
    
    # Get all scenario folders from train, val, test
    scenario_sources = [
        (train_orig, "train"),
        (val_orig, "val"),
        (test_orig, "test")
    ]
    
    for source_dir, split_name in scenario_sources:
        scenario_folders = sorted([d for d in source_dir.iterdir() if d.is_dir()])
        
        for scenario in scenario_folders:
            scenario_name = scenario.name
            print(f"\nProcessing scenario: {scenario_name} from {split_name}")
            
            # Create scenario folder in merged_100
            target_scenario = merged_folder / scenario_name
            target_scenario.mkdir(exist_ok=True)
            
            # Folders/files to link from train/val/test
            items_to_link = ["image", "lidar", "sdmap.json"]
            
            for item in items_to_link:
                source_item = source_dir / scenario_name / item
                if source_item.exists():
                    target_link = target_scenario / item
                    
                    if target_link.exists() or target_link.is_symlink():
                        print(f"  Already exists: {item}")
                    else:
                        # Create relative path
                        rel_path = os.path.relpath(source_item, target_scenario)
                        target_link.symlink_to(rel_path)
                        print(f"  Linked {item} from {split_name}")
                else:
                    print(f"  Warning: {item} not found in {split_name}/{scenario_name}")
            
            # Handle info folder - link from full_json_100/{split_name}
            source_info = info_base / split_name / scenario_name / "info"
            target_info = target_scenario / "info"
            
            if target_info.exists() or target_info.is_symlink():
                print(f"  Already exists: info")
            else:
                if source_info.exists():
                    # Link from full_json_100
                    rel_path = os.path.relpath(source_info, target_scenario)
                    target_info.symlink_to(rel_path)
                    print(f"  Linked info from full_json_100/{split_name}")
                else:
                    print(f"  Warning: info folder not found in full_json_100/{split_name}/{scenario_name}")


if __name__ == "__main__":
    create_symbolic_links()