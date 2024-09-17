from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv
from pose_detector import PoseDetector
from movement_comparator import MovementComparator
from feedback_generator import FeedbackGenerator
import json


class TelegramBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        #self.movement_comparator = MovementComparator()
        self.feedback_generator = FeedbackGenerator()

    async def folder_selected(self, update, context):
        query = update.callback_query
        await query.answer()

        # Extraer el nombre de la carpeta seleccionada del callback_data
        selected_folder = query.data.replace('folder_', '')
        
        # Obtener el directorio raíz del proyecto
        project_root = os.getcwd()
        folder_path = os.path.join(project_root, selected_folder)
        
        # Leer todos los archivos .json en la carpeta seleccionada
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

        if not json_files:
            await query.edit_message_text(text=f"No se encontraron archivos .json en la carpeta {selected_folder}.")
            return
        
        # Crear botones para cada archivo .json
        keyboard = []
        for json_file in json_files:
            json_name = json_file.replace('.json','')
            keyboard.append([InlineKeyboardButton(json_name, callback_data=f'json_{json_name}')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Editar el mensaje para mostrar los archivos .json encontrados
        await query.edit_message_text(text="Selecciona un truco:", reply_markup=reply_markup)


    # Handler para iniciar el proceso y listar carpetas
    async def start(self, update, context):
        print('Start handler triggered')
        await update.message.reply_text("¡Bienvenido! Selecciona una opción para iniciar.")

        # Obtener el directorio raíz del proyecto
        project_root = os.getcwd()

        # Obtener las carpetas dentro del directorio del proyecto y excluir "bot" y "__pycache__"
        exclude_folders = ['bot', '__pycache__']
        folders = [f for f in os.listdir(project_root) 
                if os.path.isdir(os.path.join(project_root, f)) and f not in exclude_folders]

        # Crear botones para cada carpeta
        keyboard = []
        for folder in folders:
            keyboard.append([InlineKeyboardButton(folder, callback_data=f'folder_{folder}')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data['reply_markup'] = reply_markup
        
        # Enviar el mensaje con el teclado dinámico
        await update.message.reply_text("Selecciona categoria:", reply_markup=reply_markup)

    # Handler para capturar la selección de archivos .json (opcional)
    async def json_selected(self, update, context):
        query = update.callback_query
        await query.answer()

        selected_json = query.data.replace('json_', '')
        await query.edit_message_text(text=f"Has seleccionado el archivo: {selected_json}")

        context.user_data['selected_trick'] = selected_json

        await query.message.reply_text('Por favor sube un video realizando este truco')



    async def button_handler(self, update, context):
        print('Button handler triggered')
        query = update.callback_query
        await query.answer()
        selected_trick = query.data
        self.process_trick(selected_trick)


    async def test_command(self, update, context):
        print('Test command triggered')
        await update.message.reply_text("Test command received!")

    async def video_handler(self, update, context):

        print('Video handler triggered')

        selected_trick = context.user_data.get('selected_trick', None)
        if not selected_trick:
            await update.message.reply_text('Por favor selecciona un truco antes de subir el video')
            return
        
        video_file = await update.message.video.get_file()
        
        download_directory = 'trick'
        download_path = os.path.join(download_directory,'video.mp4')

        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        video_path = await video_file.download_to_drive(download_path)

        await update.message.reply_text(f'Video subido correctamente')
        base_folder = context.user_data.get('selected_folder')

        await self.process_trick(selected_trick, video_path,base_folder,update,context)


    async def welcome_handler(self, update, context):
        print('Welcome handler triggered')
        await update.message.reply_text('¡Hola! Soy tu bot de patinaje. Puedes usar los siguientes comandos:\n\n/start - Iniciar el bot\n/tricks - Ver trucos disponibles\n/help - Obtener ayuda')

    async def process_trick(self, trick_name,video_path,base_folder,update,context):
        # Dummy implementation for processing tricks
        print(f"Processing trick: {trick_name}")
        print(base_folder)

        pose_detector = PoseDetector()

        pose_detector.process_video(video_path)
    

        # Paso 2: Cargar los landmarks de referencia (movimiento base)
        base_landmark_file = f'{base_folder}/{trick_name}.json'
        if os.path.exists(base_landmark_file):
            with open(base_landmark_file, 'r') as f:
                base_landmarks = json.load(f)
        else:
            print(f"Error: No se encontró el archivo de landmarks base: {base_landmark_file}")
            return
        
        print('comparando....')

        # Paso 3: Comparar los landmarks usando MovementComparator
        movement_comparator = MovementComparator(base_landmarks, pose_detector.pose_landmarks)
        feedback = []
        # Comparar frame a frame
        for frame_num in range(len(pose_detector.pose_landmarks)):
            diferencias = movement_comparator.calculate_differences(frame_num)
            if diferencias:
                frame_feedback = self.feedback_generator.generate_feedback(diferencias)
                feedback.extend(frame_feedback)
            else:
                print(f"No hay diferencias significativas en el frame {frame_num}")

        chat_id = update.message.chat_id
        if feedback:
            for comment in feedback:
                await context.bot.send_message(chat_id=chat_id, text =comment)
        else:
            await context.bot.send_message(chat_id=chat_id, text='truco perfecto')

        

    async def button_handler(self, update, context):
        query = update.callback_query
        await query.answer()

        selected_folder = query.data.replace('folder_','')
        context.user_data['selected_folder'] = selected_folder

        await query.edit_message_text(text=f'has seleccionado {selected_folder}')
        await self.folder_selected(update,context)


    def run(self):
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('tricks', self.welcome_handler))  # Command to list tricks
        self.application.add_handler(CommandHandler('help', self.welcome_handler))  # Command to get help
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.welcome_handler)) # Handle all text messages
        self.application.add_handler(CallbackQueryHandler(self.button_handler, pattern='^folder_'))  # Handle folder selection
        self.application.add_handler(CallbackQueryHandler(self.json_selected, pattern='^json_'))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.video_handler))

        

        print('Bot is running...')
        self.application.run_polling()

if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.run()
