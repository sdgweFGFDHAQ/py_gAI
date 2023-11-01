# 确定数据结构，暂定
## 目前认为json格式还不错，暂用csv
```
# 围绕一级属性CON STR AGI SPI INT LUK构建,衍生次级属性HP MP ATN ATT
隐藏次级属性，不用显示。目前只考虑一部分属性
id name CON STR AGI SPI INT LUK HP MP ATN ATT
```

# 初始化数据值，确定数值范围
## 属性正常数值范围
```
人物经验值系统
LEVEL
EXP
Skill Level
Skill Proficiency
```
```
CON:
STR:
AGI:
SPI:
INT:
LUK:
HP:
MP:
ATN:
ATT:
```
## 考虑处理0值负值情况

# 生成目标对象，生成成长曲线

# 创建计算公式

# 实现攻防结果

```
ATN 物理攻击力,DEF 防御力,INT 魔法攻击力,ATT 攻击力,SPD 速度，回避物理攻击；
HIT 命中率或者连击、RES 魔法防御力、STR 力量（微量增加生命值、近战伤害力）
CON 体质（增加生命值、负重力）、DEX 灵巧（增加命中率、微量减少受到的物理损伤）；
PER 感知力、LER 学识、WIL 意志力（影响生命值、法力、精力上限）
MAG 魔力、CHR 魅力 SPEED 决定角色经过多久之后是一回合，同时也影响在世界地图上的移动力、
LIFE 角色每级HP的成长率
```
