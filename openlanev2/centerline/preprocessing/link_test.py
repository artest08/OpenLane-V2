"""
Step 1 of dataset setup: Create the test/ split.

The original OpenLane-V2 dataset ships with train/, val/, and test/ folders.
Because the official test/ split lacks ground-truth annotations, this script
builds a new test/ by combining:
  - sensor data  (images, LiDAR, SD map)  from test_orig/
  - annotations  (info/*.json)             from test_gt/

Before running this script
--------------------------
1. Rename the original test/ folder to test_orig/:
       mv <data_root>/test <data_root>/test_orig

2. Download test_gt/ from the Google Drive link provided in the README and
   place it at <data_root>/test_gt/.

Expected directory layout
-------------------------
<data_root>/
├── train/
├── val/
├── test_orig/        ← renamed from the original test/
└── test_gt/          ← downloaded from Google Drive

After running this script
-------------------------
<data_root>/
└── test/             ← symlinks to test_orig/ (sensor) + test_gt/ (annotations)

Usage
-----
    python link_test.py --data_root ~/datasets/OpenLane-V2
"""

import argparse
import os
from pathlib import Path


def create_test_split(data_root: str) -> None:
    data_root = Path(data_root).expanduser().resolve()

    test_orig  = data_root / 'test_orig'
    test_gt    = data_root / 'test_gt'
    test_folder = data_root / 'test'

    if not test_orig.exists():
        print(f'Error: {test_orig} does not exist.\n'
              f'Please rename the original test/ folder to test_orig/ first.')
        return

    if not test_gt.exists():
        print(f'Error: {test_gt} does not exist.\n'
              f'Please download test_gt/ from Google Drive and place it at {test_gt}.')
        return

    test_folder.mkdir(exist_ok=True)

    scenario_folders = sorted([d for d in test_orig.iterdir() if d.is_dir()])
    print(f'Found {len(scenario_folders)} scenarios in test_orig/.')

    for scenario in scenario_folders:
        scenario_name = scenario.name
        print(f'\nProcessing scenario: {scenario_name}')

        target_scenario = test_folder / scenario_name
        target_scenario.mkdir(exist_ok=True)

        # Sensor data comes from test_orig
        for item in ['image', 'lidar', 'sdmap.json']:
            source_item = test_orig / scenario_name / item
            if source_item.exists():
                target_link = target_scenario / item
                if target_link.exists() or target_link.is_symlink():
                    print(f'  Already exists: {item}')
                else:
                    rel_path = os.path.relpath(source_item, target_scenario)
                    target_link.symlink_to(rel_path)
                    print(f'  Linked {item} from test_orig/')

        # Annotation info/ comes from test_gt if available, else test_orig
        target_info = target_scenario / 'info'
        if target_info.exists() or target_info.is_symlink():
            print('  Already exists: info/')
        else:
            test_gt_info   = test_gt   / scenario_name / 'info'
            test_orig_info = test_orig / scenario_name / 'info'
            if test_gt_info.exists():
                rel_path = os.path.relpath(test_gt_info, target_scenario)
                target_link = target_scenario / 'info'
                target_link.symlink_to(rel_path)
                print('  Linked info/ from test_gt/')
            elif test_orig_info.exists():
                rel_path = os.path.relpath(test_orig_info, target_scenario)
                target_link = target_scenario / 'info'
                target_link.symlink_to(rel_path)
                print('  Linked info/ from test_orig/')
            else:
                print('  Warning: info/ not found in test_gt/ or test_orig/')

    print('\nDone. Run link_merged.py next.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create test/ split by merging test_orig/ (sensor data) and test_gt/ (annotations).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python link_test.py --data_root ~/datasets/OpenLane-V2',
    )
    parser.add_argument(
        '--data_root',
        type=str,
        required=True,
        help='Path to the root of your OpenLane-V2 dataset (contains train/, val/, test_orig/, test_gt/).',
    )
    args = parser.parse_args()
    create_test_split(args.data_root)
