from re import sub
from src.domain.services.sanitizer import Sanitizer


class PokeNameSanitizer(Sanitizer):
    PATTERN = r"[^a-zA-Z0-9\s]"

    def sanitize(self, name):
        sanitized_name = self._replace_special_characters(name)
        sanitized_name = self._remove_special_characters(sanitized_name)
        sanitized_name = self._remove_apex_prefix(sanitized_name)
        return sanitized_name.strip()

    def _replace_special_characters(self, name):
        return name.replace("-", " ").replace("_", " ")

    def _remove_special_characters(self, name):
        return sub(self.PATTERN, "", name.lower())

    def _remove_apex_prefix(self, name):
        if name.split()[0].lower() == "apex":
            return " ".join(name.split()[1:])
        return name
