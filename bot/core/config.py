import os

_ENV_VAR_PREFIX = "MTATB_"

_debug_mode = os.environ.get(_ENV_VAR_PREFIX + "DEBUG_MODE")
debug_mode = False
if _debug_mode == "true" or _debug_mode == "True":
    debug_mode = True


api_key = os.environ.get(_ENV_VAR_PREFIX + "WOMBO_API_KEY")
if api_key is None:
    print("MTATB_WOMBO_API_KEY not set, exiting...")
    exit(1)

deezer_master_key = os.environ.get(_ENV_VAR_PREFIX + "DEEZER_MASTER_KEY")
if deezer_master_key is None:
    print("MTATB_DEEZER_MASTER_KEY not set, exiting...")
    exit(1)

mongodb_url = os.environ.get(_ENV_VAR_PREFIX + "MONGODB_URL")
if mongodb_url is None:
    print("MTATB_MONGODB_URL not set, exiting...")
    exit(1)

twitter_api_key = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_API_KEY")
if twitter_api_key is None:
    print("MTATB_TWITTER_API_KEY not set, exiting...")
    exit(1)

twitter_api_secret = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_API_SECRET")
if twitter_api_secret is None:
    print("MTATB_TWITTER_API_SECRET not set, exiting...")
    exit(1)

twitter_access_token = os.environ.get(_ENV_VAR_PREFIX + "TWITTER_ACCESS_TOKEN")
if twitter_access_token is None:
    print("MTATB_TWITTER_ACCESS_TOKEN not set, exiting...")
    exit(1)

twitter_access_token_secret = os.environ.get(
    _ENV_VAR_PREFIX + "TWITTER_ACCESS_TOKEN_SECRET"
)
if twitter_access_token_secret is None:
    print("MTATB_TWITTER_ACCESS_TOKEN_SECRET not set, exiting...")
    exit(1)
