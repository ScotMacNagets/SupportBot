
from aiogram import Router, F
from aiogram.filters import Command

from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callbacks.super_user_menu_callback import SuperuserAction, SuperuserAdminDelete, SuperuserDeleteActions, \
    SuperuserMenu
from core.text import AdminSuperuser
from keyboards.superuser_keyboard import build_superuser_menu_keyboard, build_admin_list, delete_admin_keyboard, \
    back_to_the_main_menu_keyboard
from services.admin_repo import get_all_admins, get_admin_before_delete, get_admin, superuser_check, delete_admin
from services.key_repo import generate_new_key

router = Router()

@router.message(Command("superuser_menu"))
async def superuser_menu(
        message: Message,
        session: AsyncSession,
):
    is_superuser = await superuser_check(
        session=session,
        telegram_id=message.from_user.id,
    )

    if is_superuser:
        await message.answer(
            text="Доброе пожаловать в меню супер-пользователя:",
            reply_markup=await build_superuser_menu_keyboard()
        )
        return

    await message.answer(
        text="У тебя нет доступа к этому меню"
    )

@router.callback_query(SuperuserMenu.filter(F.action == SuperuserAction.realise_new_key))
async def realise_new_key(
        query: CallbackQuery,
        callback_data: SuperuserMenuAction,
        session: AsyncSession,
):
    new_key = await generate_new_key(session=session)
    if new_key:
        await query.answer()
        await query.message.edit_text(
            text=f"Новый ключ сгенерирован: \n\n{new_key}"
        )
    else:
        await query.answer()
        await query.message.edit_text(
            text="Не удалось сгенерировать новый ключ, попробуйте позже"
        )

@router.callback_query(SuperuserMenu.filter(F.action == SuperuserAction.admin_list))
async def admin_list(
        query: CallbackQuery,
        callback_data: SuperuserMenuAction,
        session: AsyncSession,
):
    admins = await get_all_admins(session=session)
    await query.answer()
    await query.message.edit_text(
        text="Список админов (если админа нет в списке, значит он сейчас занят):",
        reply_markup=build_admin_list(admins=admins)
    )

@router.callback_query(SuperuserAdminDelete.filter(F.action == SuperuserDeleteActions.admin_delete))
    query: CallbackQuery,
    callback_data: AdminDeleteAction,
    session: AsyncSession,
):
    admin = await get_admin(
        session=session,
        telegram_id=callback_data.telegram_id
    )
    if admin:
        await query.answer()
        await query.message.edit_text(
            text=f"Admin:{admin.username} \n\n telegram_id:{admin.telegram_id} \n\n created_at:{admin.created_at}",
            reply_markup=await delete_admin_keyboard(telegram_id=admin.telegram_id)
        )
        return
    await query.answer()
    await query.message.edit_text(
        text="Админ не найден, попробуйте позже"
    )

@router.callback_query(SuperuserAdminDelete.filter(F.action == SuperuserDeleteActions.confirm_delete))
async def confirm_delete(
        query: CallbackQuery,
        callback_data: AdminDeleteAction,
        session: AsyncSession,
):
    admin = await get_admin_before_delete(
        session=session,
        telegram_id=callback_data.telegram_id
    )
    if admin:
        await query.answer()
        await query.message.edit_text(
            text=f"✅ Админ: {admin.username} успешно удален"
        )
        return
    await query.answer()
    await query.message.edit_text(
        text="Админ уже начал с кем то диалог, попробуйте позже"
    )





