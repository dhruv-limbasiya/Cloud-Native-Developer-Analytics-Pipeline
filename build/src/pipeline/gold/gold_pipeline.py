from src.core.logger import Logger

from src.storage.parquet_reader import ParquetReader
from src.storage.gold_writer import GoldWriter
from src.storage.metadata_writer import MetadataWriter

from src.pipeline.gold.repository_metrics import RepositoryMetrics
from src.pipeline.gold.language_metrics import LanguageMetrics
from src.pipeline.gold.contributor_metrics import ContributorMetrics
from src.pipeline.gold.repository_activity import RepositoryActivity
from src.pipeline.gold.organization_summary import OrganizationSummary

from src.dq.gold_validator import GoldValidator


class GoldPipeline:
    """
    Silver -> Gold Pipeline
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.reader = ParquetReader()
        self.writer = GoldWriter()
        self.metadata = MetadataWriter()
        self.validator = GoldValidator()

    def run(self, organization):

        self.logger.info("Starting Gold Pipeline")

        self.build_repository_metrics(organization)
        self.build_language_metrics(organization)
        self.build_contributor_metrics(organization)
        self.build_repository_activity(organization)
        self.build_organization_summary(organization)

        self.logger.info("Gold Pipeline Completed")
    
    # Repository Metrics

    def build_repository_metrics(self, organization):

        silver_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=repositories/"
        )

        silver_files = self.reader.read_directory(
            silver_prefix
        )

        if not silver_files:

            self.logger.warning(
                "Repositories dataset not found."
            )

            return

        for silver_file in silver_files:

            self.logger.info(
                f"Processing {silver_file['file_name']}"
            )

            dataframe = silver_file["data"]

            gold_dataframe = RepositoryMetrics.build(
                dataframe
            )

            # Temporary values
            # Later these will be parsed automatically
            year_value = "2026"
            month_value = "07"
            day_value = "22"

            output_path = self.writer.save(
                organization=organization,
                dataset="repository_metrics",
                dataframe=gold_dataframe,
                year=year_value,
                month=month_value,
                day=day_value,
            )

            self.metadata.save(
                organization=organization,
                endpoint="gold_repository_metrics",
                record_count=len(gold_dataframe),
                file_path=output_path,
                status="SUCCESS",
            )
                
    # Language Metrics

    def build_language_metrics(self, organization):

        silver_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=languages/"
        )

        silver_files = self.reader.read_directory(
            silver_prefix
        )

        if not silver_files:

            self.logger.warning(
                "Languages dataset not found."
            )

            return

        for silver_file in silver_files:

            self.logger.info(
                f"Processing {silver_file['file_name']}"
            )

            dataframe = silver_file["data"]

            gold_dataframe = LanguageMetrics.build(
                dataframe
            )

            # Temporary values
            year_value = "2026"
            month_value = "07"
            day_value = "22"

            output_path = self.writer.save(
                organization=organization,
                dataset="language_metrics",
                dataframe=gold_dataframe,
                year=year_value,
                month=month_value,
                day=day_value,
            )

            self.metadata.save(
                organization=organization,
                endpoint="gold_language_metrics",
                record_count=len(gold_dataframe),
                file_path=output_path,
                status="SUCCESS",
            )
    
    # Contributor Metrics

    def build_contributor_metrics(self, organization):

        silver_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=contributors/"
        )

        silver_files = self.reader.read_directory(
            silver_prefix
        )

        if not silver_files:

            self.logger.warning(
                "Contributors dataset not found."
            )

            return

        for silver_file in silver_files:

            self.logger.info(
                f"Processing {silver_file['file_name']}"
            )

            dataframe = silver_file["data"]

            gold_dataframe = ContributorMetrics.build(
                dataframe
            )

            # Temporary values
            year_value = "2026"
            month_value = "07"
            day_value = "22"

            output_path = self.writer.save(
                organization=organization,
                dataset="contributor_metrics",
                dataframe=gold_dataframe,
                year=year_value,
                month=month_value,
                day=day_value,
            )

            self.metadata.save(
                organization=organization,
                endpoint="gold_contributor_metrics",
                record_count=len(gold_dataframe),
                file_path=output_path,
                status="SUCCESS",
            )
                
    # Repository Activity

    def build_repository_activity(self, organization):

        commits_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=commits/"
        )

        issues_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=issues/"
        )

        pull_requests_prefix = (
            f"silver/"
            f"organization={organization}/"
            f"dataset=pull_requests/"
        )

        commit_files = self.reader.read_directory(
            commits_prefix
        )

        issue_files = self.reader.read_directory(
            issues_prefix
        )

        pr_files = self.reader.read_directory(
            pull_requests_prefix
        )

        if (
            not commit_files
            or not issue_files
            or not pr_files
        ):

            self.logger.warning(
                "Repository activity datasets not found."
            )

            return

        self.logger.info(
            "Processing Repository Activity"
        )

        commit_df = commit_files[0]["data"]
        issue_df = issue_files[0]["data"]
        pr_df = pr_files[0]["data"]

        activity = RepositoryActivity.build(
            commit_df,
            issue_df,
            pr_df
        )

        year_value = "2026"
        month_value = "07"
        day_value = "22"

        output_path = self.writer.save(
            organization=organization,
            dataset="repository_activity",
            dataframe=activity,
            year=year_value,
            month=month_value,
            day=day_value,
        )

        self.metadata.save(
            organization=organization,
            endpoint="gold_repository_activity",
            record_count=len(activity),
            file_path=output_path,
            status="SUCCESS",
        )
                
    # Organization Summary
    def build_organization_summary(self, organization):

        repository_metrics_prefix = (
            f"gold/"
            f"organization={organization}/"
            f"dataset=repository_metrics/"
        )

        language_metrics_prefix = (
            f"gold/"
            f"organization={organization}/"
            f"dataset=language_metrics/"
        )

        contributor_metrics_prefix = (
            f"gold/"
            f"organization={organization}/"
            f"dataset=contributor_metrics/"
        )

        repository_activity_prefix = (
            f"gold/"
            f"organization={organization}/"
            f"dataset=repository_activity/"
        )

        repository_files = self.reader.read_directory(
            repository_metrics_prefix
        )

        language_files = self.reader.read_directory(
            language_metrics_prefix
        )

        contributor_files = self.reader.read_directory(
            contributor_metrics_prefix
        )

        activity_files = self.reader.read_directory(
            repository_activity_prefix
        )

        if (
            not repository_files
            or not language_files
            or not contributor_files
            or not activity_files
        ):

            self.logger.warning(
                "Organization summary datasets not found."
            )

            return

        self.logger.info(
            "Processing Organization Summary"
        )

        repository_df = repository_files[0]["data"]
        language_df = language_files[0]["data"]
        contributor_df = contributor_files[0]["data"]
        activity_df = activity_files[0]["data"]

        organization_summary = OrganizationSummary.build(
            organization=organization,
            repository_df=repository_df,
            language_df=language_df,
            contributor_df=contributor_df,
            activity_df=activity_df,
        )

        year_value = "2026"
        month_value = "07"
        day_value = "22"

        output_path = self.writer.save(
            organization=organization,
            dataset="organization_summary",
            dataframe=organization_summary,
            year=year_value,
            month=month_value,
            day=day_value,
        )

        self.metadata.save(
            organization=organization,
            endpoint="gold_organization_summary",
            record_count=len(organization_summary),
            file_path=output_path,
            status="SUCCESS",
    )