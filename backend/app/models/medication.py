from tortoise import fields, models


class Medication(models.Model):
    """ 用药记录模型:记录患者的用药情况 """
    id = fields.IntField(pk=True, description="主键ID")
    # 关联患者表，一对多关系
    patient = fields.ForeignKeyField('models.Patient', related_name='medications', description="关联患者")
    drug_name = fields.CharField(max_length=100, description="药品名称")
    drug_type = fields.CharField(max_length=50, null=True, description="药品类型(口服/注射/外用等)")
    dosage = fields.CharField(max_length=50, description="单次剂量")
    frequency = fields.CharField(max_length=50, null=True, description="用药频率(每日1次/每日2次等)")
    timing = fields.TextField(null=True, description="用药时间(餐前/餐后/睡前等)")
    start_date = fields.DateField(description="开始用药日期")
    end_date = fields.DateField(null=True, description="结束用药日期")
    is_active = fields.BooleanField(default=True, description="是否正在服用")
    side_effects = fields.TextField(null=True, description="副作用记录")
    note = fields.TextField(null=True, description="备注说明")
    created_at = fields.DatetimeField(auto_now_add=True, description="录入时间")

    class Meta:
        table = "medications"