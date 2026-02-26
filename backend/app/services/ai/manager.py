import logging

from app.services.ai.base import AIProvider
from app.services.ai.kimi_provider import KimiProvider

logger = logging.getLogger(__name__)


class AIServiceManager:
    """AI 服务管理器，支持 Kimi/Gemini 双服务切换"""

    def __init__(self):
        self._providers: dict[str, AIProvider] = {}

    def _get_or_create_provider(self, name: str) -> AIProvider:
        if name not in self._providers:
            if name == "kimi":
                self._providers["kimi"] = KimiProvider()
            elif name == "gemini":
                # 懒加载 Gemini（需要安装 google-generativeai）
                try:
                    from app.services.ai.gemini_provider import GeminiProvider
                    self._providers["gemini"] = GeminiProvider()
                except ImportError:
                    logger.warning("google-generativeai not installed, falling back to Kimi")
                    self._providers["gemini"] = KimiProvider()
            else:
                raise ValueError(f"Unknown AI provider: {name}")
        return self._providers[name]

    def get_provider(self, preference: str = "kimi") -> AIProvider:
        """根据用户偏好获取 AI 服务提供者

        Args:
            preference: kimi / gemini / auto
                - kimi: 使用 Kimi（国内用户推荐）
                - gemini: 使用 Gemini（海外用户推荐）
                - auto: 默认使用 Kimi，失败时降级到 Gemini
        """
        if preference == "auto":
            preference = "kimi"
        return self._get_or_create_provider(preference)

    def get_provider_name(self, preference: str = "kimi") -> str:
        if preference == "auto":
            return "kimi"
        return preference


ai_manager = AIServiceManager()
