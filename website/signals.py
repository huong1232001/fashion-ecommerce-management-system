# website/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import MProduct, TOrderCart

@receiver(post_save, sender=MProduct)
def update_order_cart_on_product_save(sender, instance, **kwargs):
    print(f"Signal chạy update cart: {instance.product_name}")
    
    # Cập nhật giỏ hàng khi sản phẩm thay đổi (cập nhật tên, mô tả, giá, hình ảnh)
    TOrderCart.objects.filter(product=instance).update(
        product_name=instance.product_name,
        description=instance.description,
        product_image=instance.image,
        product_price=instance.price
    )

@receiver(pre_save, sender=MProduct)
def delete_order_cart_on_product_soft_delete(sender, instance, **kwargs):
    try:
        old_instance = MProduct.objects.get(pk=instance.pk)
    except MProduct.DoesNotExist:
        return

    # Nếu sản phẩm bị xóa mềm (delete_flag = True) hoặc hiển thị bị tắt (display_flag = False)
    if (not old_instance.delete_flag and instance.delete_flag) or (old_instance.display_flag and not instance.display_flag):
        # Xóa các sản phẩm trong giỏ hàng có liên quan
        TOrderCart.objects.filter(product=instance).delete()
