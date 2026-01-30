import re
from typing import Set
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat
from parser.utils.config import config
from email_validator import validate_email, EmailNotValidError

class ContactExtractor:

    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    PHONE_PATTERN = re.compile(
        r"""
        (?:
            \+?\d{1,3}[\s\-()]*
        )?
        (?:
            \d{2,4}[\s\-()]*
        ){2,4}
        \d{2,4}
        """,
        re.VERBOSE,
    )

    @classmethod
    def extract_emails(cls, text: str) -> Set[str]:
        raw_emails = set(cls.EMAIL_PATTERN.findall(text))
        valid_emails = set()

        for email in raw_emails:
            if email.lower().endswith((".webp", ".png", ".jpg", ".svg")):
                continue
            try:
                validate_email(email)
                valid_emails.add(email.lower())
            except EmailNotValidError:
                continue
        return valid_emails


    @classmethod
    def extract_phones(cls, text: str) -> Set[str]:
        if not text:
            return set()

        raw_phones = set(match.group(0) for match in cls.PHONE_PATTERN.finditer(text))

        cleaned_phones = set()
        for phone in raw_phones:
            normalized = cls._normalize_phone(phone)
            if normalized:
                cleaned_phones.add(normalized)

        return cleaned_phones

    @staticmethod
    def _normalize_phone(phone: str) -> str | None:
        try:
            parsed = phonenumbers.parse(phone, config.phone_region)
            if not phonenumbers.is_valid_number(parsed):
                return None
            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        except NumberParseException:
            return None
