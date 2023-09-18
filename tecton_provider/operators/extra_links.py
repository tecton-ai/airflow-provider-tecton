from airflow.models import BaseOperator, BaseOperatorLink


class RegistryLink(BaseOperatorLink):
    """Link to Registry"""

    name = "Astronomer Registry"

    def get_link(self, operator, dttm):
        """Get link to registry page."""

        return (
            f"https://registry.astronomer.io/providers/airflow-provider-fivetran-async/versions/"
            f"{__version__}/modules/{operator.operator_name}"
        )

