from .user import UserAdmin
from .group import GroupAdmin
from .event import EventAdmin
from .attendance import AttendanceAdmin

admin_views = [UserAdmin, GroupAdmin, EventAdmin]
custom_views = [AttendanceAdmin]
