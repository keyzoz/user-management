from src.db.models import Roles, User


def is_admin(current_user: User):
    if current_user.role == Roles.USER_ADMIN:
        return True
    return False


def is_moderator(current_user: User):
    if current_user.role == Roles.USER_MODERATOR:
        return True
    return False


def is_moderator_of_target_group_or_admin(current_user: User, target_user: User):
    if is_moderator(current_user) and is_admin(target_user):
        return False
    if (
        is_moderator(current_user) and current_user.group_name == target_user.group_name
    ) or is_admin(current_user):
        return True
    return False


def is_admin_or_moderator_of_target_group(current_user: User, target_user: User):
    if (
        is_moderator(current_user) and current_user.group_name == target_user.group_name
    ) or (is_admin(current_user) and current_user.group_name == target_user.group_name):
        return True
    return False
