from tortoise import fields, models


class Exercise(models.Model):
    """ 运动记录模型:记录患者的运动情况 """
    id = fields.IntField(pk=True, description="主键ID")
    # 关联患者表，一对多关系
    patient = fields.ForeignKeyField('models.Patient', related_name='exercise_records', description="关联患者")
    exercise_type = fields.CharField(max_length=50, description="运动类型(跑步/游泳/瑜伽等)")
    duration_min = fields.IntField(description="运动时长(分钟)")
    intensity = fields.CharField(max_length=20, default="中等", description="运动强度(低/中等/高)")
    calories_burned = fields.FloatField(null=True, description="消耗热量(kcal)")
    performed_at = fields.DatetimeField(description="运动时间")
    blood_sugar_before = fields.FloatField(null=True, description="运动前血糖(mmol/L)")
    blood_sugar_after = fields.FloatField(null=True, description="运动后血糖(mmol/L)")
    note = fields.TextField(null=True, description="备注说明")
    created_at = fields.DatetimeField(auto_now_add=True, description="录入时间")

    class Meta:
        table = "exercise_records"

    @property
    def bs_change(self) -> float:
        """ 计算血糖变化 """
        if self.blood_sugar_before and self.blood_sugar_after:
            return round(self.blood_sugar_after - self.blood_sugar_before, 1)
        return 0.0

