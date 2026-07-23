DQ_CONFIG = {

    "repositories": {

        "required_columns": [
            "repository_id",
            "repository_name"
        ],

        "duplicate_column": "repository_id",

        "numeric_columns": [
            "stars",
            "forks",
            "watchers"
        ]
    },

    "languages": {

        "required_columns": [
            "repository_name",
            "language"
        ],

        "duplicate_column": None,

        "numeric_columns": [
            "bytes_of_code"
        ]
    },

    "contributors": {

        "required_columns": [
            "contributor_id",
            "repository_name"
        ],

        "duplicate_column": None,

        "numeric_columns": [
            "contributions"
        ]
    },

    "commits": {

        "required_columns": [
            "commit_sha",
            "repository_name"
        ],

        "duplicate_column": "commit_sha",

        "numeric_columns": None
    },

    "issues": {

        "required_columns": [
            "issue_id",
            "repository_name"
        ],

        "duplicate_column": "issue_id",

        "numeric_columns": [
            "issue_comments"
        ]
    },

    "pull_requests": {

        "required_columns": [
            "pull_request_id",
            "repository_name"
        ],

        "duplicate_column": "pull_request_id",

        "numeric_columns": [
            "comments",
            "commits",
            "additions",
            "deletions",
            "changed_files"
        ]
    }

}