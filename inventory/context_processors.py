def user_roles(request):
    user = request.user

    if not user.is_authenticated:
        return {
            'is_admin_role': False,
            'is_merchandiser_role': False,
            'is_seller_role': False,
        }

    is_admin_role = user.is_superuser or user.groups.filter(name='Администратор').exists()
    is_merchandiser_role = user.groups.filter(name='Мерчендайзер').exists()
    is_seller_role = user.groups.filter(name='Продавец').exists()

    return {
        'is_admin_role': is_admin_role,
        'is_merchandiser_role': is_merchandiser_role,
        'is_seller_role': is_seller_role,
    }
