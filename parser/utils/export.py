import csv


class Exporter:

    def __init__(self, result: dict):
        self.result = result

    def to_csv(self, filename: str) -> None:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["url", "emails", "phones"])
            writer.writerow([
                self.result["url"],
                ";".join(self.result["emails"]),
                ";".join(self.result["phones"])
            ])

    def to_txt(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"URL: {self.result['url']}\n\n")
            f.write("Emails:\n")
            for email in self.result["emails"]:
                f.write(f"{email}\n")
            f.write("\nPhones:\n")
            for phone in self.result["phones"]:
                f.write(f"{phone}\n")
