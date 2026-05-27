from utilities.choices import ChoiceSet


class ProxyProtocolChoices(ChoiceSet):
    HTTP = "http"
    HTTPS = "https"
    GRPC = "grpc"
    FASTCGI = "fastcgi"

    CHOICES = (
        (HTTP, "HTTP", "cyan"),
        (HTTPS, "HTTPS", "green"),
        (GRPC, "gRPC", "blue"),
        (FASTCGI, "FastCGI", "purple"),
    )


class ProxyBalanceChoices(ChoiceSet):
    ROUND_ROBIN = "round_robin"
    LEAST_CONN = "least_conn"
    IP_HASH = "ip_hash"
    RANDOM = "random"

    CHOICES = (
        (ROUND_ROBIN, "Round Robin", "cyan"),
        (LEAST_CONN, "Least Connections", "green"),
        (IP_HASH, "IP Hash", "blue"),
        (RANDOM, "Random", "purple"),
    )


class ProxySSLModeChoices(ChoiceSet):
    OFF = "off"
    ON = "on"
    STRICT = "strict"

    CHOICES = (
        (OFF, "Off", "gray"),
        (ON, "On", "green"),
        (STRICT, "Strict", "blue"),
    )


class ProxyCertProviderChoices(ChoiceSet):
    MANUAL = "manual"
    LETSENCRYPT = "letsencrypt"
    SELFSIGNED = "selfsigned"

    CHOICES = (
        (MANUAL, "Manual", "gray"),
        (LETSENCRYPT, "Let's Encrypt", "green"),
        (SELFSIGNED, "Self-Signed", "orange"),
    )


class LocationMatchTypeChoices(ChoiceSet):
    MATCH_PREFIX = "prefix"
    MATCH_EXACT = "exact"
    MATCH_REGEX = "regex"
    MATCH_REGEX_ICASE = "regex_icase"

    CHOICES = (
        (MATCH_PREFIX, "Prefix", "cyan"),
        (MATCH_EXACT, "Exact", "green"),
        (MATCH_REGEX, "Regex", "orange"),
        (MATCH_REGEX_ICASE, "Regex (case-insensitive)", "purple"),
    )


class DeployStatusChoices(ChoiceSet):
    STATUS_PENDING = "pending"
    STATUS_RENDERING = "rendering"
    STATUS_TESTING = "testing"
    STATUS_DEPLOYING = "deploying"
    STATUS_RELOADING = "reloading"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_ROLLED_BACK = "rolled_back"

    CHOICES = (
        (STATUS_PENDING, "Pending", "cyan"),
        (STATUS_RENDERING, "Rendering", "blue"),
        (STATUS_TESTING, "Testing", "yellow"),
        (STATUS_DEPLOYING, "Deploying", "orange"),
        (STATUS_RELOADING, "Reloading", "purple"),
        (STATUS_SUCCESS, "Success", "green"),
        (STATUS_FAILED, "Failed", "red"),
        (STATUS_ROLLED_BACK, "Rolled Back", "gray"),
    )
