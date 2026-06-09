from utils.utils import load_influencers

influencers = load_influencers()

ID_MAP = {
    inf["id"]: inf
    for inf in influencers
}