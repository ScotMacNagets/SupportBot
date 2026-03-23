
from aiogram import Router, F
from aiogram.enums import ParseMode
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
            text=AdminSuperuser.WELCOME_TO_SUPERUSER_MENU,
            reply_markup=await build_superuser_menu_keyboard()
        )
        return

    await message.answer(
        text=AdminSuperuser.NOT_ENOUGH_RIGHTS,
    )

@router.callback_query(SuperuserMenu.filter(F.action == SuperuserAction.realise_new_key))
async def realise_new_key(
        query: CallbackQuery,
        session: AsyncSession,
):
    new_key = await generate_new_key(session=session)
    if new_key:
        await query.answer()
        await query.message.edit_text(
            text=AdminSuperuser.NEW_KEY_GENERATED.format(
                new_key=new_key,
            ),
            reply_markup= await back_to_the_main_menu_keyboard(),
            parse_mode=ParseMode.HTML,
        )
    else:
        await query.answer()
        await query.message.edit_text(
            text=AdminSuperuser.CANNOT_GENERATE_THE_KEY,
            reply_markup= await back_to_the_main_menu_keyboard()
        )

@router.callback_query(SuperuserMenu.filter(F.action == SuperuserAction.admin_list))
async def admin_list(
        query: CallbackQuery,
        session: AsyncSession,
):
    admins = await get_all_admins(session=session)
    await query.answer()
    await query.message.edit_text(
        text=AdminSuperuser.ADMIN_LIST,
        reply_markup=await build_admin_list(admins=admins)
    )

@router.callback_query(SuperuserAdminDelete.filter(F.action == SuperuserDeleteActions.admin_delete))
async def delete_admin_handler(
    query: CallbackQuery,
    callback_data: SuperuserAdminDelete,
    session: AsyncSession,
):
    admin = await get_admin(
        session=session,
        telegram_id=callback_data.telegram_id
    )
    if admin:
        await query.answer()
        await query.message.edit_text(
            text=AdminSuperuser.ADMIN_FORMAT_DETAIL.format(
                telegram_id=admin.telegram_id,
                username=admin.username,
                created_at=admin.created_at,
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=await delete_admin_keyboard(telegram_id=admin.telegram_id),
        )
        return
    await query.answer()
    await query.message.edit_text(
        text=AdminSuperuser.ADMIN_NOT_FOUND,
        reply_markup= await back_to_the_main_menu_keyboard()
    )

@router.callback_query(SuperuserAdminDelete.filter(F.action == SuperuserDeleteActions.confirm_delete))
async def confirm_delete(
        query: CallbackQuery,
        callback_data: SuperuserAdminDelete,
        session: AsyncSession,
):
    admin = await get_admin_before_delete(
        session=session,
        telegram_id=callback_data.telegram_id
    )
    if admin:
        await delete_admin(
            session=session,
            telegram_id=callback_data.telegram_id
        )
        await query.answer()
        await query.message.edit_text(
            text=AdminSuperuser.SUCCESSFULLY_DELETED.format(
                username=admin.username,
            )
        )
        return
    await query.answer()
    await query.message.edit_text(
        text=AdminSuperuser.ADMIN_IS_BUSY,
        reply_markup=await back_to_the_main_menu_keyboard()
        )

@router.callback_query(F.data == SuperuserAction.back_to_the_main_menu)
async def back_to_the_main_menu(
    query: CallbackQuery,
):
    await query.message.edit_text(
        text=AdminSuperuser.WELCOME_TO_SUPERUSER_MENU,
        reply_markup=await build_superuser_menu_keyboard()
    )







