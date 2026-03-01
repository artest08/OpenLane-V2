import os
from pathlib import Path


def create_symbolic_links():
    # Source directories
    test_orig = Path("/media/hdd/esat_datasets/test_json/test_orig")
    test_gt = Path("/media/hdd/esat_datasets/test_json/test_gt")

    # Target directory
    test_folder = Path("/media/hdd/esat_datasets/test_json/test")
    test_folder.mkdir(exist_ok=True)

    # Get all scenario folders from test_orig
    if not test_orig.exists():
        print(f"Error: {test_orig} does not exist")
        return

    scenario_folders = sorted([d for d in test_orig.iterdir() if d.is_dir()])

    for scenario in scenario_folders:
        scenario_name = scenario.name
        print(f"\nProcessing scenario: {scenario_name}")

        # Create scenario folder in test
        target_scenario = test_folder / scenario_name
        target_scenario.mkdir(exist_ok=True)

        # Folders/files to link from test_orig
        items_to_link = ["image", "lidar", "sdmap.json"]

        for item in items_to_link:
            source_item = test_orig / scenario_name / item
            if source_item.exists():
                target_link = target_scenario / item

                if target_link.exists() or target_link.is_symlink():
                    print(f"  Already exists: {item}")
                else:
                    # Create relative path
                    rel_path = os.path.relpath(source_item, target_scenario)
                    target_link.symlink_to(rel_path)
                    print(f"  Linked {item} from test_orig")

        # Handle info folder - check test_gt first, then test_orig
        test_gt_info = test_gt / scenario_name / "info"
        test_orig_info = test_orig / scenario_name / "info"
        target_info = target_scenario / "info"

        if target_info.exists() or target_info.is_symlink():
            print(f"  Already exists: info")
        else:
            if test_gt_info.exists():
                # Link from test_gt
                rel_path = os.path.relpath(test_gt_info, target_scenario)
                target_info.symlink_to(rel_path)
                print(f"  Linked info from test_gt")
            elif test_orig_info.exists():
                # Link from test_orig
                rel_path = os.path.relpath(test_orig_info, target_scenario)
                target_info.symlink_to(rel_path)
                print(f"  Linked info from test_orig")
            else:
                print(f"  Warning: info folder not found in test_gt or test_orig")


if __name__ == "__main__":
    create_symbolic_links()