"""
DataClean Pro - Advanced Data Cleaning and Preprocessing Toolkit
Created by: Duncan Nyabaro
GitHub: https://github.com/DopeJ/data-cleaning-toolkit

A comprehensive data cleaning utility that handles common data quality issues
with professional logging, validation, and multiple processing strategies.
"""

import pandas as pd
import numpy as np
import logging
from typing import Union, List, Dict, Any, Optional
from pathlib import Path
import warnings
from scipy import stats
from sklearn.preprocessing import StandardScaler, LabelEncoder
import re

class DataCleanPro:
    """
    Advanced Data Cleaning and Preprocessing Toolkit
    Created by: Duncan Nyabaro
    Version: 1.0.0

    Features:
    - Missing value imputation with multiple strategies
    - Outlier detection and treatment
    - Data type optimization
    - Duplicate detection and removal
    - Text normalization and cleaning
    - DateTime parsing and feature engineering
    - Data validation and quality reporting
    """

    def __init__(self, df: pd.DataFrame = None):
        """
        Initialize DataCleanPro with a DataFrame

        Args:
            df (pd.DataFrame): Input DataFrame to clean
        """
        self.df = df
        self.original_shape = df.shape if df is not None else None
        self.cleaning_report = {}

        # Set up professional logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - DataCleanPro - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger('DataCleanPro')

        self.logger.info("DataClean Pro initialized - Created by Duncan Nyabaro")

    def handle_missing_values(self, strategy: Dict[str, Any] = None) -> 'DataCleanPro':
        """Handle missing values with various strategies"""
        if strategy is None:
            strategy = {}

        self.logger.info("Handling missing values using smart imputation")

        for column in self.df.columns:
            if self.df[column].isnull().any():
                # Use provided strategy or default to median for numeric and mode for non-numeric
                col_strategy = strategy.get(column, 'median' if np.issubdtype(self.df[column].dtype, np.number) else 'mode')

                try:
                    if col_strategy == 'mean':
                        self.df[column].fillna(self.df[column].mean(), inplace=True)
                    elif col_strategy == 'median':
                        self.df[column].fillna(self.df[column].median(), inplace=True)
                    elif col_strategy == 'mode':
                        mode_val = self.df[column].mode()
                        if not mode_val.empty:
                            self.df[column].fillna(mode_val[0], inplace=True)
                        else:
                            self.df[column].fillna('Unknown', inplace=True)
                    else:
                        # If it's a value, use it
                        self.df[column].fillna(col_strategy, inplace=True)
                except Exception as e:
                    self.logger.warning(f"Could not fill missing values for {column} with {col_strategy}: {e}")

        return self

    def remove_duplicates(self, subset: List[str] = None, keep: str = 'first') -> 'DataCleanPro':
        """Remove duplicate rows"""
        self.logger.info("Removing duplicate records")
        duplicates_before = self.df.duplicated(subset=subset).sum()
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        duplicates_after = self.df.duplicated(subset=subset).sum()
        self.cleaning_report['duplicates_removed'] = duplicates_before - duplicates_after
        self.logger.info(f"Removed {duplicates_before - duplicates_after} duplicate rows")
        return self

    def get_cleaning_report(self) -> Dict[str, Any]:
        """Generate cleaning report"""
        if self.original_shape:
            final_shape = self.df.shape
            self.cleaning_report.update({
                'original_shape': self.original_shape,
                'final_shape': final_shape,
                'rows_removed': self.original_shape[0] - final_shape[0],
                'columns_removed': self.original_shape[1] - final_shape[1],
            })
        return self.cleaning_report

    def auto_clean(self) -> 'DataCleanPro':
        """Run automatic cleaning pipeline"""
        self.logger.info("Starting automatic data cleaning pipeline...")
        return self.handle_missing_values().remove_duplicates()
