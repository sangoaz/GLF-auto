from typing import Type
from sqlmodel import Session, SQLModel, select


def get_images_for_parent(
    session: Session,
    image_model: Type[SQLModel],
    parent_field: str,
    parent_id: int,
):
    field = getattr(image_model, parent_field)
    statement = select(image_model).where(field == parent_id)
    return session.exec(statement).all()


def insert_image_with_order(
    session: Session,
    image_model: Type[SQLModel],
    parent_field: str,
    parent_id: int,
    new_image,
):
    images = get_images_for_parent(session, image_model, parent_field, parent_id)

    max_order = len(images)
    new_order = max(0, min(new_image.display_order, max_order))

    for image in images:
        if image.display_order >= new_order:
            image.display_order += 1

    new_image.display_order = new_order
    session.add(new_image)

    return new_image


def reorder_image(
    session: Session,
    image_model: Type[SQLModel],
    parent_field: str,
    parent_id: int,
    target_image,
    new_order: int,
):
    images = get_images_for_parent(session, image_model, parent_field, parent_id)

    old_order = target_image.display_order
    max_order = len(images) - 1
    new_order = max(0, min(new_order, max_order))

    if new_order == old_order:
        return target_image

    if new_order < old_order:
        for image in images:
            if (
                image.id != target_image.id
                and new_order <= image.display_order < old_order
            ):
                image.display_order += 1

    elif new_order > old_order:
        for image in images:
            if (
                image.id != target_image.id
                and old_order < image.display_order <= new_order
            ):
                image.display_order -= 1

    target_image.display_order = new_order
    return target_image


def delete_image_with_reindex(
    session: Session,
    image_model: Type[SQLModel],
    parent_field: str,
    parent_id: int,
    target_image,
):
    deleted_order = target_image.display_order
    images = get_images_for_parent(session, image_model, parent_field, parent_id)

    session.delete(target_image)

    for image in images:
        if image.id != target_image.id and image.display_order > deleted_order:
            image.display_order -= 1


def set_cover_image(
    session: Session,
    image_model: Type[SQLModel],
    parent_field: str,
    parent_id: int,
    target_image,
):
    images = get_images_for_parent(session, image_model, parent_field, parent_id)

    for image in images:
        image.is_cover = image.id == target_image.id

    return target_image
