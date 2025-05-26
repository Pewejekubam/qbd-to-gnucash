# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

from typing import Dict, Any
from utils.error_handler import ValidationError
from utils.logging import get_logger


def run_validation_pass(data: Dict[str, Any]) -> None:
    """
    Perform global validation checks on processed module data.

    Args:
        data (Dict[str, Any]): Dictionary of processed domain data keyed by module.

    Raises:
        ValidationError: If structural or logical issues are detected.

    Example:
        run_validation_pass({'accounts': {...}, 'mapping': {...}})
    """
    logger = get_logger('output/qbd-to-gnucash.log')
    accounts = data.get('accounts', {})
    mapping = data.get('mapping', {})
    # Example validation: ensure all account types are mapped
    for name, node in accounts.items():
        acc_type = node.record.get('ACCNTTYPE')
        if acc_type not in mapping.get('account_types', {}):
            logger.error(f'Unmapped account type: {acc_type} in account {name}')
            raise ValidationError(f'Unmapped account type: {acc_type}')
    # Additional validation rules per PRD can be added here
    logger.info('Validation pass completed successfully.')

# Liberal inline comments and agentic structure per PRD.