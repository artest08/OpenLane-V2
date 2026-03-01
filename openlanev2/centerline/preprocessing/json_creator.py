from openlanev2.centerline.io import io
import json

# # Near Split
# folder_path = "/home/ek21/git/data-leakage/near_extrapolation_splits/argoverse2/argo_geo_txts"
# split_dict = {'train': 'train.txt', 'val': 'val.txt', 'test': 'test.txt'}


folder_path = "/home/ek21/git/data-leakage/far_extrapolation_splits/argoverse2"
# farA Split
# split_dict = {'train': 'PIT+MIA.txt', 'val': 'REST.txt'}
# # farB Split
# split_dict = {'train': 'MIA+REST.txt', 'val': 'PIT.txt'}
# # farC Split
split_dict = {'train': 'PIT+REST.txt', 'val': 'MIA.txt'}



# get the contents of the folder which are like train.txt, val.txt, test.txt
# These txt files includes scenario ids
# create a scenario id dict to hold the scenario ids for each split

scenario_id_dict = {}
for split_name, file_name in split_dict.items():
    with open(f"{folder_path}/{file_name}", 'r') as f:
        scenario_ids = f.read().splitlines()  # read all scenario ids from the file
    scenario_id_dict[split_name] = scenario_ids  # add to the dict


root_path = 'data/Subset-A-ls'
data = io.json_load(f"{root_path}/data_dict_subset_A.json")
data_new = {}
for split in data.keys():
    data_new[split] = {}


for split, segments in data.items():
    for segment_id in segments.keys():
        print(f"Processing segment: {segment_id} in split: {split}")
        timestamp = segments[segment_id][0]
        sample = io.json_load(f'{root_path}/{split}/{segment_id}/info/{timestamp}')
        scenario_id = sample["meta_data"]["source_id"]
        for split_name, scenario_ids in scenario_id_dict.items():
            if scenario_id in scenario_ids:
                data_new[split_name][segment_id] = segments[segment_id]
                break

# Dump the data_new to a json file properly with open
with open(f"{root_path}/data_dict_subset_A_farC.json", 'w') as f:
    json.dump(data_new, f, indent=4)
