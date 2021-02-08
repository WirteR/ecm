from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from db.account.models import Translation
from db.core.models import BaseModel, User
from db.payment.models import Account
# Create your models here.


class ProductCategory(MPTTModel):
    translations = models.ManyToManyField(Translation, related_name="categories")

    key = models.CharField(max_length=125, null=True, blank=True)
    uid = models.CharField(max_length=125, null=True, blank=True)
    avatar = models.ImageField(upload_to="category-images")
    name = models.CharField(max_length=256)
    description = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uid} | {self.name}" 


class ProductAttribute(BaseModel):
    user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    translations = models.ManyToManyField(Translation, related_name="attributes")
    
    name = models.CharField(max_length=128)
    description = models.TextField()
    terms = models.TextField()
    user_owner = models.ForeignKey(User, related_name="attribute", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    translations = models.ManyToManyField(Translation, related_name="tags")
    
    name = models.CharField(max_length=128)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class QualityData(BaseModel):
    condition = models.CharField(max_length=128)
    quality_text = models.CharField(max_length=128)
    quality_description = models.TextField()

    def __str__(self):
        return self.condition


class QualityImage(BaseModel):
    exp = models.ForeignKey(QualityData, related_name="quality_images", on_delete=models.CASCADE)
    quality_image = models.ImageField(upload_to="product-images")


class Product(BaseModel):
    #alternative_images - serializer
    attributes = models.ManyToManyField(ProductAttribute, related_name="products", blank=True)
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.SET_NULL, null=True)
    translations = models.ManyToManyField(Translation, related_name="products")
    tags = models.ManyToManyField(ProductTag, related_name="products", blank=True)
    user_owner = models.ForeignKey(User, related_name="products", on_delete=models.SET_NULL, null=True)
    quality_data = models.ForeignKey(QualityData, related_name="products", on_delete=models.SET_NULL, null=True)

    standart_price = models.DecimalField(max_digits=7, decimal_places=2)
    title = models.CharField(max_length=125)
    description = models.TextField()
    type = models.CharField(max_length=125, null=True)
    sku = models.CharField(max_length=125)
    marketplace_sku = models.CharField(max_length=125)

    main_image = models.ImageField(upload_to="product-images")
    extra_data = models.JSONField()

    @property
    def serialized(self):
        pass

    def __str__(self):
        return f"{self.sku} | {self.title}"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")


class ProductService(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    purchase_price = models.DecimalField(max_digits=7, decimal_places=2)
    price_gross = models.DecimalField(max_digits=7, decimal_places=2)
    price_net = models.DecimalField(max_digits=7, decimal_places=2)
    price_tax = models.DecimalField(max_digits=7, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    default_import = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    

# class ProductData(models.Model):
#     brand = models.CharField(max_length=125)
#     designer = models.CharField(max_length=125)
#     manufacturer = models.CharField(max_length=125, null=True, blank=True)
#     bullet_point = models.CharField(max_length=10)
#     merchant_catalog_number = models.CharField(max_length=25)
#     serial_number_req = models.CharField(125)
#     legal_disclamer = models.TextField()
#     mfr_part_number = models.CharField(max_length=25)
#     search_terms = models.TextField()
#     platinum_keywords = models.TextField()
#     browse_node = models.CharField(126)
#     memorabilia = models.CharField(126)
#     autographed = models.BooleanField(default=False)
#     other_item_attributes = models.CharField(max_length=256)
#     target_audience = models.CharField(max_length=125)
#     subject_content = models.TextField()
#     TSD_age_warning = models.CharField(max_length=24)
#     TSD_warning = models.CharField(max_length=128)	
#     TSD_language = models.CharField(max_length=24)
#     product_data = models.CharField(max_length=512)    
#     variation = models.CharField(max_length=128)
#     exp = models.CharField(max_length=128)