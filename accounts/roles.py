from rolepermissions.roles import AbstractUserRole

CREATE_RIDE = 'create_ride'
VIEW_RIDE_HISTORY = 'view_ride_history'
ACCEPT_RIDE = 'accept_ride'
class Driver(AbstractUserRole):
    available_permissions = {
        ACCEPT_RIDE:True
    }


class Customer(AbstractUserRole):
    available_permissions ={
        CREATE_RIDE:True,
        VIEW_RIDE_HISTORY:True,

    }