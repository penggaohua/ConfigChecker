#命名规则 Test_ +表名，这个类检查“ChapterConfig.xlsx”这个配置表
class Test_ChapterConfig(ConfigBase):

    #todo 想办法精简这部分
    def setup_class(self):
        self.check_table = os.path.basename(__file__).split('.')[0].split('_')[1]+".xlsx"#根据文件名得到表名
        ConfigBase.setup_class_base(self,self.check_table)


    #为空检查 - 所有列都检查
    def test_null_all_column(self,get_head_list):
        for column_name in get_head_list:
             self.check_null(column_name)

    #为空检查 - 检查指定列
    @pytest.mark.parametrize("column_name",['id','name','picture'])
    def test_null(self,column_name):
        self.check_null(column_name)

    #重复检查：比如id列name列不能重复
    @pytest.mark.parametrize("column_name", ["id","name"])
    def test_repeat(self,column_name):
        self.check_repeat(column_name)

    #格式检查
    @pytest.mark.parametrize("column_name,regex",[("picture","PanelWar/zx_img\d+")])
    def test_regext(self,column_name,regex):
        self.check_regext(column_name,regex)

    #值域检查
    @pytest.mark.parametrize("column_name,min,max",[("id",1,15)])
    def test_range(self,column_name,min,max):
        self.check_range(column_name,min,max)
