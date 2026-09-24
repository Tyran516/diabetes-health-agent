from tortoise import fields, models


class DietRecord(models.Model):
    """ 饮食记录模型:记录患者的饮食摄入情况 """
    id = fields.IntField(pk=True, description="主键ID")
    # 关联患者表，一对多关系
    patient = fields.ForeignKeyField('models.Patient', related_name='diet_records', description="关联患者")
    food_name = fields.CharField(max_length=100, description="食物名称")
    calories = fields.FloatField(null=True, description="热量(kcal)")
    carbs = fields.FloatField(null=True, description="碳水化合物(g)")
    protein = fields.FloatField(null=True, description="蛋白质(g)")
    fat = fields.FloatField(null=True, description="脂肪(g)")
    gi_value = fields.FloatField(null=True, description="血糖生成指数(GI)")
    portion = fields.FloatField(default=1.0, description="分数/重量")
    meal_type = fields.CharField(max_length=20, null=True, description="餐次类型(早餐/午餐/晚餐/加餐)")
    eaten_at = fields.DatetimeField(description="进食时间")
    note = fields.TextField(null=True, description="备注说明")
    created_at = fields.DatetimeField(auto_now_add=True, description="录入时间")

    class Meta:
        table = "diet_records"

    @property
    def gi_level(self) -> str:
        """ 判断食物的GI等级 """
        if self.gi_value is None:return "未知"
        if self.gi_value <= 55:return "低GI"
        if self.gi_value <= 70:return "中GI"
        return "高GI"

    
