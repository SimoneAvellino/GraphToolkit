from abc import ABC, abstractmethod


class DistributionStratetegy(ABC):

    @abstractmethod
    def get(self):
        """Return the next edge according to the distribution strategy."""
        pass


def distribution_factory(dist_str: str) -> DistributionStratetegy:
    # examinate dist_str to detect which distribution to use and the parameters
    if dist_str.startswith("gaussian"):
        from distributions.gaussian import (
            GaussianDistribution,
        )  # local import to avoid circular dependency

        # Example dist_str: "gaussian(mean=0,stddev=1)"
        params_str = dist_str[len("gaussian(") : -1]
        params = {}
        for param in params_str.split(","):
            key, value = param.split("=")
            params[key.strip()] = float(value.strip())

        return GaussianDistribution(mean=params["mean"], stddev=params["stddev"])
    else:
        raise ValueError(f"Unsupported distribution strategy: {dist_str}")
