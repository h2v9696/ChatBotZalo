from rivescript import RiveScript

bot = RiveScript(utf8=True)
bot.load_directory("engine/eg/brain")
bot.sort_replies()

class BotManager:
    @staticmethod
    def reply(msg):
        response = bot.reply("teabot", msg)
        return response
