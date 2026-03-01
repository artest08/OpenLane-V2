import os
from pathlib import Path

root_path = '/media/hdd/esat_datasets/olv2_merged'
# In the root path there are train val test folder
# In each folder, there are scenearios like 00000, 00001
# what I want is linking all these scenario folder to a folder named merged so that can be reached within a single folder


def create_symbolic_links():
    # Source directories
    train_orig = Path(os.path.join(root_path, "train"))
    val_orig = Path(os.path.join(root_path, "val"))
    test_orig = Path(os.path.join(root_path, "test"))

    # Target directory
    merged_folder = Path(os.path.join(root_path, "merged"))
    merged_folder.mkdir(exist_ok=True)

    # Get all scenario folders from train, val, test
    if not train_orig.exists() or not val_orig.exists() or not test_orig.exists():
        print(f"Error: One of the source directories does not exist")
        return

    scenario_folders = sorted([d for d in train_orig.iterdir() if d.is_dir()]) + \
                       sorted([d for d in val_orig.iterdir() if d.is_dir()]) + \
                       sorted([d for d in test_orig.iterdir() if d.is_dir()])

    # Link structure should be relative target
    for scenario in scenario_folders:
        scenario_name = scenario.name
        print(f"\nProcessing scenario: {scenario_name}")

        # Create scenario folder in merged
        target_scenario = merged_folder / scenario_name

        # Determine source folder
        if (train_orig / scenario_name).exists():
            source_scenario = train_orig / scenario_name
        elif (val_orig / scenario_name).exists():
            source_scenario = val_orig / scenario_name
        elif (test_orig / scenario_name).exists():
            source_scenario = test_orig / scenario_name
        else:
            print(f"  Error: Scenario {scenario_name} not found in any source directories")
            continue

        # rel path from target to source
        rel_path = os.path.relpath(source_scenario, target_scenario.parent)
        target_scenario.symlink_to(rel_path)


if __name__ == "__main__":
    create_symbolic_links()
