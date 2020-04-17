from ICantineManagerDB import InfoStudentsDB


db = InfoStudentsDB()
db.InfoStudentsCreateTable()
#db.InfoStudentsAdd(("Kilian", "Stockinger", "4G", "Kilian.Stockinger.png"))
db.InfoStudentsDeleteNULL()
db.InfoStudentsCommit()

db.InfoStudentsQueryAll()
db.InfoStudentsClose()
