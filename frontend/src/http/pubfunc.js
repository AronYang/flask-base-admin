//说明：该文件用来存放公共函数


// 校验IP的函数
export const checkIP = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入IP'));
      } else {
        var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
        console.log(reg.test(value), 'check ip')
        if (reg.test(value) == 1) {
          callback()
          // this.$refs.ruleForm.validateField('ip')
        } else {
          callback(new Error('请输入正确的IP'))
        }
      }
    };