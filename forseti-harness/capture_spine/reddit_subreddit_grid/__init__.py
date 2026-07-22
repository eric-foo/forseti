"""Reddit subreddit grid: listing-page projection and registry materialization.

The grid lane captures one subreddit listing page (best/top/rising/hot/new)
as a Source Capture Packet (``source_family="reddit_subreddit_grid"``) and
derives from it, read-only:

- a grid view (venue envelope + thread rows with visible engagement), and
- Reddit Subreddit Registry refreshes under the registry spec's two-speed
  rule (observations append; descriptive facts update-on-change).

Owner contracts:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_spec_v0.md
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
"""

from capture_spine.reddit_subreddit_grid.grid_projection import (
    GridThreadRow,
    GridView,
    RedditGridProjectionError,
    project_old_reddit_grid_html,
)
from capture_spine.reddit_subreddit_grid.materializer import (
    LakeRefreshOutcome,
    RegistryRefreshOutcome,
    RegistryRefreshError,
    read_grid_packet,
    refresh_lake_registry_from_grid_packets,
    refresh_registry_from_grid_packets,
)

__all__ = [
    "GridThreadRow",
    "GridView",
    "RedditGridProjectionError",
    "RegistryRefreshError",
    "RegistryRefreshOutcome",
    "LakeRefreshOutcome",
    "project_old_reddit_grid_html",
    "read_grid_packet",
    "refresh_lake_registry_from_grid_packets",
    "refresh_registry_from_grid_packets",
]
