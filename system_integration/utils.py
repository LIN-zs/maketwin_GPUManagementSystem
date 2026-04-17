import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

logger = logging.getLogger(__name__)

def notify_gpu_update(action="update", gpu_id=None):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gpu_updates",
            {
                "type": "send_update",
                "data": {
                    "action": action,
                    "gpu_id": gpu_id,
                    "timestamp": str(timezone.now())
                }
            }
        )
    except Exception as e:
        # 仅记录错误，不抛出，避免影响 HTTP 响应
        logger.error(f"WebSocket 推送失败（不影响业务）: {e}")