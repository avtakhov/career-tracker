from .user import UserAdmin
from .group import GroupAdmin
from .event import EventAdmin

admin_views = [UserAdmin, GroupAdmin, EventAdmin]
