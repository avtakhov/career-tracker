from .purchase import PurchaseAdmin
from .user import UserAdmin
from .group import GroupAdmin
from .event import EventAdmin
from .attendance import AttendanceAdmin
from .product import ProductAdmin


admin_views = [UserAdmin, GroupAdmin, EventAdmin, ProductAdmin, PurchaseAdmin]
custom_views = [AttendanceAdmin]
