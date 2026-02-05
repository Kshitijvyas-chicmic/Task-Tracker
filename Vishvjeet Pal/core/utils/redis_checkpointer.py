# core/utils/redis_checkpointer.py
from langgraph.checkpoint.redis import RedisSaver
from core.utils.config import settings

# Manual entry to get the BaseCheckpointSaver instance
_saver_context = RedisSaver.from_conn_string(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)
checkpointer = _saver_context.__enter__()
