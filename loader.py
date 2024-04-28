import pandas as pd

def load_dataset(subreddit, prefix="data/clean/"):
    df = pd.read_pickle(prefix+subreddit+".pkl")
    return df

def get_dataset_names(experiment):
    experiment_datasets = {
        "feminism_incel": ["feminism_full", "incels_full"],
        "feminism_over_time": ["feminism_2015_2017", "feminism_2017_2019", "feminism_2019_2021", "feminism_2021_2023"],
        "within_feminism": ["feminism_full", "fourthwavewomen", "blackladies", "feminisms", "feminismuncensored", "women", "fireyfemmes"], 
        # same as within incels due to migration across subreddits over time
        "incels_over_time": ["incels", "braincels", "trufemcels", "mensrights"], # add theredpill
    }
    if experiment not in experiment_datasets:
        return ["incels", "braincels", "trufemcels", "mensrights", "incels_full","feminism_full", "feminism_2015_2017", "feminism_2017_2019", "feminism_2019_2021", "feminism_2021_2023", "fourthwavewomen", "blackladies", "feminisms", "feminismuncensored", "women", "fireyfemmes"]
    return experiment_datasets[experiment]