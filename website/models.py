from django.db import models
from django.utils import timezone

class MUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "m_user_management"
class UserPassword(models.Model):
    user_password_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MUser, on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return f"Password for {self.user.user_name}"

    class Meta:
        db_table = 'user_password'  # Liên kết đúng bảng
class MProductType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
    type_code = models.CharField(max_length=50, blank=True, null=True, unique=True)  # ➡️ thêm cột type_code
    note = models.CharField(max_length=255, blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'm_product_type'
class MProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    type = models.ForeignKey(MProductType, on_delete=models.CASCADE)
    type_code = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=100, default='')
    quality_inventory_of_size_S = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quality_inventory_of_size_M = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quality_inventory_of_size_L = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quality_inventory_of_freesize = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cột mới
    quality_inventory_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #status_flag = models.BooleanField(default=True)
    display_flag = models.BooleanField(default=True)
    delete_flag = models.BooleanField(default=False)
    is_freesize = models.BooleanField(default=False)
    product_code = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Tự động tính tổng tồn kho tùy theo loại sản phẩm
        if self.is_freesize:
            self.quality_inventory_total = self.quality_inventory_of_freesize
        else:
            self.quality_inventory_total = (
                self.quality_inventory_of_size_S +
                self.quality_inventory_of_size_M +
                self.quality_inventory_of_size_L
            )
        # Cập nhật type_code nếu có type
        if self.type:
            self.type_code = self.type.type_code

        super(MProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'm_product'

class TProductFavorite(models.Model):
    user = models.ForeignKey('MUser', on_delete=models.CASCADE)  # Khóa ngoại liên kết MUser
    product = models.ForeignKey('MProduct', on_delete=models.CASCADE)  # Khóa ngoại liên kết MProduct
    favorite_flag = models.BooleanField(default=True)  # Mặc định là True khi thêm vào danh sách yêu thích
    delete_flag = models.BooleanField(default=False)  # Đánh dấu soft delete (không xóa hẳn)

    class Meta:
        db_table = 't_product_favorite'  # Tên bảng trong database
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_favorite')
        ]  # Đảm bảo mỗi cặp user - product là duy nhất (tạo khóa chính kép)

    def __str__(self):
        return f"User {self.user_id} - Product {self.product_id} (Favorite: {self.favorite_flag})"
class TOrderCart(models.Model):
    order_cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('MUser', on_delete=models.CASCADE)  # Liên kết đến MUser
    product = models.ForeignKey('MProduct', on_delete=models.CASCADE)  # Liên kết đến MProduct
    product_name = models.CharField(max_length=255)  # Lưu tên sản phẩm
    description = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.CharField(max_length=255)  # Lưu đường dẫn ảnh sản phẩm
    product_size = models.CharField(max_length=10)  # Lưu kích thước sản phẩm (S, M, L, ...)
    product_quality_cart = models.PositiveIntegerField(default=1)  # Số lượng sản phẩm trong giỏ
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    delete_flag = models.BooleanField(default=False)  # Soft delete

    class Meta:
        db_table = 't_order_cart'  # Tên bảng trong database

    def __str__(self):
        return f"{self.user.user_name} - {self.product_name} ({self.product_size})"
class ManagerAccount(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'm_manager_account'  # Tên bảng trong database

class ManagerPassword(models.Model):
    user_password_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(ManagerAccount, on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return f"Password for {self.user.user_name}"

    class Meta:
        db_table = 'manager_password'  # Tên bảng trong database
class TOrderPayment(models.Model):
    order_payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('MUser', on_delete=models.CASCADE)  # Liên kết đến MUser
    product = models.ForeignKey('MProduct', on_delete=models.CASCADE)  # Liên kết đến MProduct
    product_name = models.CharField(max_length=255)  # Lưu tên sản phẩm
    description = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.CharField(max_length=255)  # Lưu đường dẫn ảnh sản phẩm
    product_size = models.CharField(max_length=10)  # Lưu kích thước sản phẩm (S, M, L, ...)
    product_quality_payment = models.PositiveIntegerField(default=1)  # Số lượng sản phẩm trong đơn thanh toán
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    delete_flag = models.BooleanField(default=False)  # Soft delete

    class Meta:
        db_table = 't_order_payment'  # Tên bảng trong database

    def __str__(self):
        return f"{self.user.user_name} - {self.product_name} ({self.product_size})"
class MMethodPayment(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=100)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.method_name

    class Meta:
        db_table = 'm_method_payment'  # Tên bảng trong cơ sở dữ liệu
class TOrderWaitConfirmHeader(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("MUser", on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    order_date = models.DateField(default=timezone.now)
    estimated_delivery_date = models.DateField()
    total_price_order = models.DecimalField(max_digits=15, decimal_places=2)  # ✅ đổi thành Decimal
    payment_method = models.ForeignKey("MMethodPayment", on_delete=models.SET_NULL, null=True)
    delete_flag = models.BooleanField(default=False)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "t_order_wait_confirm_header"

    def __str__(self):
        return f"Order {self.order_id} - {self.user_name}"


class TOrderWaitConfirmDetail(models.Model):
    order = models.ForeignKey("TOrderWaitConfirmHeader", on_delete=models.CASCADE)
    product = models.ForeignKey("MProduct", on_delete=models.CASCADE)
    product_size = models.CharField(max_length=10)
    type = models.ForeignKey("MProductType", on_delete=models.SET_NULL, null=True)
    quality = models.DecimalField(max_digits=10, decimal_places=2)
    price_product = models.DecimalField(max_digits=15, decimal_places=2)  # ✅ đổi thành Decimal
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "t_order_wait_confirm_detail"
        unique_together = (("order", "product", "product_size"),)

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product.product_name} ({self.product_size})"


class TOrderHeader(models.Model):
    order_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        "MUser",
        on_delete=models.CASCADE
    )

    user_name = models.CharField(
        max_length=255
    )

    order_date = models.DateField(
        default=timezone.now
    )

    estimated_delivery_date = models.DateField()

    total_price_order = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_method = models.ForeignKey(
        "MMethodPayment",
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.ForeignKey(
        "MStatus",
        on_delete=models.SET_NULL,
        null=True,
        db_column='status_id'
    )

    delete_flag = models.BooleanField(
        default=False
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "t_order_header"
class TOrderDetail(models.Model):
    order = models.ForeignKey("TOrderHeader", on_delete=models.CASCADE)  # 🔹 Liên kết đến bảng đơn hàng chính thức
    product = models.ForeignKey("MProduct", on_delete=models.CASCADE)
    product_size = models.CharField(max_length=10)
    type = models.ForeignKey("MProductType", on_delete=models.SET_NULL, null=True)
    quality = models.DecimalField(max_digits=10, decimal_places=2)
    price_product = models.DecimalField(max_digits=15, decimal_places=2)
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "t_order_detail"
        unique_together = (("order", "product", "product_size"),)

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product.product_name} ({self.product_size})"
class MStatus(models.Model):

    status_id = models.CharField(
        max_length=2,
        primary_key=True
    )

    status_name = models.CharField(
        max_length=50
    )

    delete_flag = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'm_status'

    def __str__(self):
        return self.status_name
class TOrderStatus(models.Model):
    order_status_id = models.AutoField(
        primary_key=True
    )

    order = models.ForeignKey(
        TOrderHeader,
        on_delete=models.CASCADE,
        db_column='order_id'
    )

    current_status = models.ForeignKey(
        MStatus,
        on_delete=models.CASCADE,
        db_column='current_status_id',
        related_name='current_status_logs'
    )

    new_status = models.ForeignKey(
        MStatus,
        on_delete=models.CASCADE,
        db_column='new_status_id',
        related_name='new_status_logs'
    )

    note = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    delete_flag = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 't_order_status'
class THistory(models.Model):

    order_history_id = models.AutoField(
        primary_key=True
    )

    order = models.ForeignKey(
        TOrderHeader,
        on_delete=models.CASCADE,
        db_column='order_id'
    )

    user = models.ForeignKey(
        MUser,
        on_delete=models.CASCADE,
        db_column='user_id'
    )

    product = models.ForeignKey(
    MProduct,
    on_delete=models.CASCADE,
    db_column='product_id',
    null=True,
    blank=True
)

    current_order_size = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    new_order_size = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    current_quantity = models.IntegerField(
        null=True,
        blank=True
    )

    new_quantity = models.IntegerField(
        null=True,
        blank=True
    )

    current_estimate_date = models.DateField(
        null=True,
        blank=True
    )

    new_estimate_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    delete_flag = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 't_history'
