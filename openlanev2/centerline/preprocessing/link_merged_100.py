"""
Step 3 of dataset setup (±100 m splits only): Create the merged_100/ directory.

This script is only needed if you want to use the long-range splits:
    data/Subset-A-100/
    data/Subset-A-near-100/

These splits extend the perception range from the standard ±50 m to ±100 m.
The annotations for this extended range live in a separate full_json_100/
folder (downloaded from Google Drive) because the annotation pipeline was
re-run with a wider range parameter.

For each scenario the merged_100/ directory contains:
  - image/, lidar/, sdmap.json  →  symlinks into train/ / val/ / test/
  - info/                       →  symlink into full_json_100/{split}/

Expected directory layout
-------------------------
<data_root>/
├── train/
├── val/
├── test/              ← created by link_test.py
└── full_json_100/     ← downloaded from Google Drive
      ├── train/
      ├── val/
      └── test/

After running this script
-------------------------
<data_root>/
└── merged_100/        ← sensor data from splits + annotations from full_json_100/

Then create a symlink inside each relevant data/Subset-A-*-100/ folder:
    ln -s <data_root>/merged_100  <repo>/data/Subset-A-100/merged_100
    ln -s <data_root>/merged_100  <repo>/data/Subset-A-near-100/merged_100

Usage
-----
    python link_merged_100.py --data_root ~/datasets/OpenLane-V2
"""

import argparse
import os
from pathlib import Path


def create_merged_100(data_root: str) -> None:
    data_root = Path(data_root).expanduser().resolve()

    split_dirs = {
        'train': data_root / 'train',
        'val':   data_root / 'val',
        'test':  data_root / 'test',
    }
    full_json_100 = data_root / 'full_json_100'
    merged_100_dir = data_root / 'merged_100'

    for name, split_dir in split_dirs.items():
        if not split_dir.exists():
            print(f'Error: {split_dir} does not exist. Run link_test.py first.')
            return

    if not full_json_100.exists():
        print(f'Error: {full_json_100} does not exist.\n'
              f'Please download full_json_100/ from Google Drive and place it at {full_json_100}.')
        return

    merged_100_dir.mkdir(exist_ok=True)

    for split_name, split_dir in split_dirs.items():
        scenario_folders = sorted([d for d in split_dir.iterdir() if d.is_dir()])
        print(f'\nProcessing {len(scenario_folders)} scenarios from {split_name}/')

        for scenario in scenario_folders:
            scenario_name = scenario.name
            print(f'  Scenario: {scenario_name}')

            target_scenario = merged_100_dir / scenario_name
            target_scenario.mkdir(exist_ok=True)

            # Sensor data comes from the original split
            for item in ['image', 'lidar', 'sdmap.json']:
                source_item = split_dir / scenario_name / item
                if source_item.exists():
                    target_link = target_scenario / item
                    if target_link.exists() or target_link.is_symlink():
                        print(f'    Already exists: {item}')
                    else:
                        rel_path = os.path.relpath(source_item, target_scenario)
                        target_link.symlink_to(rel_path)
                        print(f'    Linked {item} from {split_name}/')
                else:
                    print(f'    Warning: {item} not found in {split_name}/{scenario_name}')

            # Annotation info/ comes from full_json_100 (re-annotated for ±100 m range)
            source_info = full_json_100 / split_name / scenario_name / 'info'
            target_info  = target_scenario / 'info'
            if target_info.exists() or target_info.is_symlink():
                print('    Already exists: info/')
            elif source_info.exists():
                rel_path = os.path.relpath(source_info, target_scenario)
                target_info.symlink_to(rel_path)
                print(f'    Linked info/ from full_json_100/{split_name}/')
            else:
                print(f'    Warning: info/ not found in full_json_100/{split_name}/{scenario_name}')

    print('\nDone.')
    print(f'Create a symlink inside each ±100 m data/ folder pointing to {merged_100_dir}:')
    for subset in ['Subset-A-100', 'Subset-A-near-100', 'Subset-A-farA-100', 'Subset-A-farB-100', 'Subset-A-farC-100']:
        print(f'  ln -s {merged_100_dir}  <repo>/data/{subset}/merged_100')
    print(f'Then run the corresponding preprocess.py scripts.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create merged_100/ for ±100 m range splits using full_json_100/ annotations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python link_merged_100.py --data_root ~/datasets/OpenLane-V2',
    )
    parser.add_argument(
        '--data_root',
        type=str,
        required=True,
        help='Path to the root of your OpenLane-V2 dataset (contains train/, val/, test/, full_json_100/).',
    )
    args = parser.parse_args()
    create_merged_100(args.data_root)
