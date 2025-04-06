
from langchain_core.documents import Document




sample_documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc", "publish_date":2020},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc",  "publish_date":2021},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc",  "publish_date":2022},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc",  "publish_date":2023},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc", "publish_date":2024},
    ),
]

question_answers_examples = [
    Document(
        page_content="'topic':考试得分是多少' topic_expansion':考试得分；考试的名字；考试班级平均得分；学生考试提交状态（未交，准时提交，迟交）；每道题得分；知识点正确率 ；班级整体得分；每道题班级整体得分；考试作答时间（单位秒）",
        metadata={"scene": "考试"},
    ),
    Document(
        page_content="'topic':作业正确率是多少' topic_expansion':作业正确率；作业的名字；作业班级平均正确率；学生作业提交状态（未交，准时提交，迟交）；每道题正确率；知识点正确率 ；班级整体正确率；每道题班级整体正确率；作业作答时间（单位秒）",
        metadata={"scene": "作业"},
    ),
    Document(
        page_content="'topic':作业有没有用心' topic_expansion': 作业是否提交；完成率；班级提交率，班级完成率；作答时长；平均作答时长；每道题的作答时长，班级平均每道题时长；正确率；班级平均正确率；最近7次正确率'",
                metadata={"scene": "作业"},
    ),
    Document(
        page_content="'topic':周末学习时长多少' topic_expansion': '作业时长、个性化练习时长、导学时长、订正时长、举一反三时长、作文时长、单词默写时长?'",
               metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三"},
    ),
    Document(
        page_content="'topic':课后有看课堂回顾吗' topic_expansion': '看课堂回顾总时长、次数、每次看课堂回顾时长；课程内容'",
        metadata={"scene": "上课"},
    ),
    Document(
        page_content="'topic':这次成绩如何'topic_expansion': 作业正确率；作业的名字；作业班级平均正确率；学生作业提交状态（未交，准时提交，迟交）；每道题的题目id及正确率；知识点正确率 ；班级整体正确率；每道题班级整体正确率；作业作答时间（单位秒）",
           metadata={"scene": "作业, 考试"},
    )
]



qa_examples_using_topic_expansion_as_page_content = [
    # 搞定
    Document(
        page_content="考试得分是多少",
        metadata={"scene": "考试", "topic_expansion":"考试得分；考试的名字；考试班级平均得分；每道题的题目id及作答时长；每道题班级平均得分；考试作答时间（单位秒）"},
    ),
    # 搞定
    Document(
        page_content="作业正确率是多少",
        metadata={"scene": "作业",  "topic_expansion": "作业正确率; 作业的名字; 作业班级平均正确率; 作业提交状态（未交，准时提交，迟交）; 每道题的题目id及作答时长;  作业作答时间总时长（单位秒）"}, 
    ),
    # 搞定
    Document(
        page_content="作业有没有用心",
                metadata={"scene": "作业", "topic_expansion":"作业名称；作业提交状态（未交，准时提交，迟交）; 作业完成率; 班级作业提交率; 班级作业完成率; 作答时长（单位秒）; 平均作答时长; 每道题的题目id及作答时长; 班级平均每道题时长; 作业正确率; 班级平均正确率; 最近7次作业的名字及正确率"},
    ),
    # 搞定
    Document(
        page_content="课后有看课堂回顾吗",
        metadata={"scene": "上课", "topic_expansion": "课堂回顾内容和时长; 每次看课堂回顾时长; 课程内容"},
    ),
    # 搞定
    Document(
        page_content="每周用多久做错题订正",
        metadata={"scene": "作业",  "topic_expansion": "从昨天开始过去四周里，每周的错题订正时长累计（单位为分钟）; 从昨天开始过去四周里，订正错题数"},
    ),
    # 搞定
    Document(
        page_content="有打开App吗",
        metadata={"scene": "作业", "topic_expansion":"上个周末的课堂回顾时长; 上个周末的作业提交数量是否为零; 他上个周末的举一反三的提交数量是否为零"},
    ),
    # 搞定
    Document(
        page_content="这次成绩是多少",
        metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"最近一次考试的名字; 考试成绩; 考试全班平均成绩; 考试答题时长是多少（单位为秒） 学生考试每一题用时分布; 考试单题得分;"},
    ),
    # TODO: 原版，缺考试年级平均成绩，考试成绩排名，考试完成率，考试知识点正确率
    # Document(
    #     page_content="这次成绩是多少",
    #     metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"最近一次考试的名字; 考试成绩; 考试全班平均成绩; 考试年级平均成绩; 考试成绩班级排名; 考试答题时长是多少（单位为秒）；考试完成率; 学生考试每一题用时分布; 考试单题得分; 考试知识点正确率"},
    # ),
    # 搞定
    Document(
        page_content="昨天作业写得好吗",
        metadata={"scene": "上课", "topic_expansion": "昨天的作业是否提交; 昨天的作业完成率; 昨天的班级提交率; 昨天的班级完成率; 昨天的作业作答时长; 昨天的作业每道题作答时长是多少？他昨天班级平均每道题作答时长是多少？他昨天的作业正确率是多少？他昨天的作业班级平均正确率是多少？他最近七次的作业正确率是多少？"},
    ),
    
    # 搞定
    Document(
        page_content="有做举一反三的练习吗",
           metadata={"scene": "举一反三" , "topic_expansion":"最近一个月做举一反三的次数; 最近一个月做举一反三的正确率"},
    ),
    # Document(
    #     page_content="昨天作业哪不会",
    #     metadata={"scene": "作业",  "topic_expansion": "昨天的班级作业正确率; 昨天的班级作业提交率; 昨天的班级作业完成率; 昨天的作业题目正确率"},
    # ),

    # Document(
    #     page_content="该月进步的原因是什么",
    #             metadata={"scene": "作业", "topic_expansion":"最近一个月的导学浏览时长; 最近一个月的作业正确率; 最近一个月的个人作业完成率; 最近一个月的个人考试得分率; 最近一个月的错题订正次数; 最近一个月的错题重做次数; 最近一个月做的举一反三题目数; 最近一个月做的个性化练习题目数"},
    # ),
    # Document(
    #     page_content="学生自主学习情况怎样",
    #            metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"最近一个月的错题订正次数; 最近一个月的错题重做次数; 最近一个月做的举一反三题目数; 最近一个月做的个性化练习题目数; 最近一个月的班级平均错题订正次数; 最近一个月的班级平均错题重做次数; 最近一个月的班级平均举一反三题目数; 最近一个月的班级平均个性化练习题目数"},
    # ),
     # TODO: 缺数据太多
    # Document(
    #     page_content="学习时长",
    #            metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"作业作答时间（单位秒）; 个性化练习作答时间（单位秒）; 导学作答时间（单位秒）; 作业订正作答时间（单位秒）; 举一反三作答时间（单位秒）; 作文时长作答时间（单位秒）; 单词默写作答时间（单位秒）"},
    # ),
    # TODO: 这类问题其实还要老师的名字才能正确筛选出来
    # Document(
    #     page_content="本次作业哪位同学最短完成",
    #     metadata={"scene": "上课", "topic_expansion": "在老师的科目下，最近一次作业中作业用时最短的学生; 用时最短的学生的每道题的正确率; 在老师的科目下，最近一次作业中整体正确率"},
    # ),
    # TODO: 知识点累的估计都没有
    # Document(
    #     page_content="在哪些题目上容易丢分",
    #        metadata={"scene": "作业, 考试" , "topic_expansion":"正确率最低的五个知识点; 这些知识点对应的错题"},
    # ),
]

# TODO: 目标
# qa_examples_using_topic_expansion_as_page_content = [
#     Document(
#         page_content="考试得分是多少",
#         metadata={"scene": "考试", "topic_expansion":"考试得分；考试的名字；考试班级平均得分；学生考试提交状态（未交，准时提交，迟交）；每道题得分；知识点正确率 ；班级整体得分；每道题班级整体得分；考试作答时间（单位秒）"},
#     ),
#     Document(
#         page_content="作业正确率是多少",
#         metadata={"scene": "作业",  "topic_expansion": "作业正确率; 作业的名字; 作业班级平均正确率; 作业提交状态（未交，准时提交，迟交）; 学生个人每道题正确率; 知识点正确率; 每道题班级整体正确率; 作业作答时间总时长（单位秒, 输出时转换为分钟）"},
#     ),
#     Document(
#         page_content="作业有没有用心",
#                 metadata={"scene": "作业", "topic_expansion":"作业名称；作业提交状态（未交，准时提交，迟交）; 作业完成率; 班级提交率; 班级完成率; 作答时长（单位秒）; 平均作答时长; 每道题的题目id及作答时长; 班级平均每道题时长; 作业正确率; 班级平均正确率; 最近7次作业的名字及正确率"},
#     ),
#     Document(
#         page_content="学习时长",
#                metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"作业作答时间（单位秒）; 个性化练习作答时间（单位秒）; 导学作答时间（单位秒）; 作业订正作答时间（单位秒）; 举一反三作答时间（单位秒）; 作文时长作答时间（单位秒）; 单词默写作答时间（单位秒）"},
#     ),
#     Document(
#         page_content="课后有看课堂回顾吗",
#         metadata={"scene": "上课", "topic_expansion": "课堂回顾总时长; 课堂回顾总次数; 每次看课堂回顾时长; 课程内容"},
#     ),
#     Document(
#         page_content="每周用多久做错题订正",
#         metadata={"scene": "作业",  "topic_expansion": "从昨天开始过去四周里，每周的错题订正时长累计（单位为分钟）; 从昨天开始过去四周里，订正错题数"},
#     ),
#     Document(
#         page_content="有打开App吗",
#         metadata={"scene": "作业", "topic_expansion":"上个周末的课堂回顾时长; 上个周末的作业提交数量是否为零; 他上个周末的举一反三的提交数量是否为零"},
#     ),
#     Document(
#         page_content="这次成绩是多少",
#                metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"最近一次考试成绩; 最近一次考试全班平均成绩; 最近一次考试年级平均成绩; 最近一次考试成绩排名; 最近一次考试答题时长是多少（单位为秒）; 最近一次考试完成率; 最近一次考试每一题用时分布; 最近一次考试单题得分率; 最近一次考试知识点正确率"},
#     ),
#     Document(
#         page_content="昨天作业写得好吗",
#         metadata={"scene": "上课", "topic_expansion": "昨天的作业是否提交; 昨天的作业完成率; 昨天的班级提交率; 昨天的班级完成率; 昨天的作业作答时长; 昨天的作业每道题作答时长是多少？他昨天班级平均每道题作答时长是多少？他昨天的作业正确率是多少？他昨天的作业班级平均正确率是多少？他最近七次的作业正确率是多少？"},
#     ),
#     Document(
#         page_content="有做举一反三的练习吗",
#            metadata={"scene": "作业, 考试" , "topic_expansion":"最近一个月做举一反三的次数; 最近一个月做举一反三的正确率"},
#     ),
#     # Document(
#     #     page_content="昨天作业哪不会",
#     #     metadata={"scene": "作业",  "topic_expansion": "昨天的班级作业正确率; 昨天的班级作业提交率; 昨天的班级作业完成率; 昨天的作业题目正确率"},
#     # ),
#     Document(
#         page_content="学生该月进步的原因是什么",
#                 metadata={"scene": "作业", "topic_expansion":"最近一个月的导学浏览时长; 最近一个月的作业正确率; 最近一个月的作业完成率; 最近一个月的考试得分率; 最近一个月的错题订正次数; 最近一个月的错题重做次数; 最近一个月做的举一反三题目数; 最近一个月做的个性化练习题目数"},
#     ),
#     Document(
#         page_content="学生自主学习情况怎样",
#                metadata={"scene": "作业, 个性化练习, 导学, 错题订正, 举一反三", "topic_expansion":"最近一个月的错题订正次数; 最近一个月的错题重做次数; 最近一个月做的举一反三题目数; 最近一个月做的个性化练习题目数; 最近一个月的班级平均错题订正次数; 最近一个月的班级平均错题重做次数; 最近一个月的班级平均举一反三题目数; 最近一个月的班级平均个性化练习题目数"},
#     ),
#     Document(
#         page_content="本次作业哪位同学最短完成",
#         metadata={"scene": "上课", "topic_expansion": "在老师的科目下，最近一次作业中作业用时最短的学生; 用时最短的学生的每道题的正确率; 在老师的科目下，最近一次作业中整体正确率"},
#     ),
#     Document(
#         page_content="在哪些题目上容易丢分",
#            metadata={"scene": "作业, 考试" , "topic_expansion":"正确率最低的五个知识点; 这些知识点对应的错题"},
#     ),
# ]