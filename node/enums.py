from enum import Enum

class NodeAction(str, Enum):
    auth = 'auth'
    get_data = 'get_data'

class Resource(str, Enum):
    customer = 'Customer'

class Operation(str, Enum):
    index_ = 'index'
    create = 'create'
    update = 'update'

class Parameters(str, Enum):
    id = 'id'
    is_study = 'is_study'
    study_status_id ='study_status_id'
    name = 'name'
    gender = 'gender'
    age_from = 'age_from'
    age_to = 'age_to'
    phone = 'phone'
    legal_type = 'legal_type'
    legal_name = 'legal_name'
    company_id = 'company_id'
    lesson_count_from ='lesson_count_from'
    lesson_count_to = 'lesson_count_to'
    balance_contract_from = 'balance_contract_from'
    balance_contract_to = 'balance_contract_to'
    balance_bonus_from = 'balance_bonus_from'
    balance_bonus_to = 'balance_bonus_to'
    removed = 'removed'
    removed_from = 'removed_from'
    removed_to = 'removed_to'
    level_id = 'level_id'
    assigned_id = 'assigned_id'
    employee_id = 'employee_id'
    lead_source_id = 'lead_source_id'
    color = 'color'
    note = 'note'
    date_from = 'date_from'
    date_to = 'date_to'
    next_lesson_date_from = 'next_lesson_date_from'
    next_lesson_date_to = 'next_lesson_date_to'
    tariff_till_from = 'tariff_till_from'
    tariff_till_to = 'tariff_till_to'
    customer_reject_id = 'customer_reject_id'
    comment = 'comment'
    dob_from = 'dob_from'
    dob_to = 'dob_to'
    withGroups_true = 'withGroups:true'
    page = 'page'
    