import os
import click
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import fadeout
from PyQt5.QtWidgets import QApplication, QFileDialog

def parse_time(time_str):
    """Parse a time string in mm.ss or ss format and return the time in seconds."""
    if '.' in time_str:
        minutes, seconds = time_str.split('.')
        return int(minutes) * 60 + int(seconds)
    else:
        return int(time_str)

class VideoEditorCLI:
    def __init__(self):
        self.video_files = []
        self.segments = {}  # Store segments as {video_index: [(start1, end1), ...]}
        self.video_clips = []
        self.segment_order = []  # Store the order of segments as [(video_index, segment_index), ...]

    def add_video(self, file_path):
        video_index = len(self.video_files)
        self.video_files.append(file_path)
        self.video_clips.append(VideoFileClip(file_path))
        self.segments[video_index] = []
        click.echo(f"Vidéo ajoutée : {file_path}")

    def add_segment(self, video_index, start_time, end_time):
        video_index -= 1  # Convert to 0-based index
        if video_index < len(self.video_files):
            start_seconds = parse_time(start_time)
            end_seconds = parse_time(end_time)
            self.segments[video_index].append((start_seconds, end_seconds))
            click.echo(f"Segment ajouté à la vidéo {video_index + 1}: Start {start_seconds} s, End {end_seconds} s")
        else:
            click.echo("Index vidéo non valide.")

    def list_segments(self):
        for video_index, segs in self.segments.items():
            file_name = os.path.basename(self.video_files[video_index])
            for i, (start, end) in enumerate(segs):
                click.echo(f"Vidéo {video_index + 1} ({file_name}), Segment {i + 1}: Start {start} s, End {end} s")

    def list_videos(self):
        for i, file_path in enumerate(self.video_files):
            click.echo(f"Vidéo {i + 1}: {os.path.basename(file_path)}")

    def set_segment_order(self, order):
        order_list = [(int(pair.split(':')[0]) - 1, int(pair.split(':')[1]) - 1) for pair in order.split(',')]
        if all(video_index < len(self.video_files) and segment_index < len(self.segments[video_index])
               for video_index, segment_index in order_list):
            self.segment_order = order_list
            click.echo("Ordre des segments mis à jour.")
        else:
            click.echo("Erreur: Un des indices de segment spécifiés est hors limites.")

    def merge_videos(self, output_path):
        if not self.segment_order:
            click.echo("Aucun ordre de segment défini. Impossible de fusionner.")
            return
        final_clips = []
        try:
            for video_index, segment_index in self.segment_order:
                start, end = self.segments[video_index][segment_index]
                clip = self.video_clips[video_index].subclip(start, end)
                final_clips.append(clip)
            final_clip = concatenate_videoclips(final_clips, method="compose")
            final_clip = self.fade_out(final_clip, duration=4)  # Apply fade out
            final_clip.write_videofile(output_path, audio_codec="aac")
            click.echo(f"Vidéos fusionnées et sauvegardées dans : {output_path}")
        except IndexError:
            click.echo("Erreur de fusion : vérifiez que tous les indices de segment sont valides.")

    def fade_out(self, clip, duration=4):
        """Apply a fade-out effect to the video and audio of the clip."""
        return fadeout(clip, duration)

    def show_stats(self):
        """Display statistics about the video segments and final film."""
        total_duration = 0
        click.echo("\nStatistiques des segments:")
        for video_index, segs in self.segments.items():
            file_name = os.path.basename(self.video_files[video_index])
            for i, (start, end) in enumerate(segs):
                duration = end - start
                total_duration += duration
                click.echo(f"Vidéo {video_index + 1} ({file_name}), Segment {i + 1}: Durée {duration} secondes (de {start} s à {end} s)")
        click.echo(f"\nNombre total de segments: {sum(len(segs) for segs in self.segments.values())}")
        click.echo(f"Durée totale du film: {total_duration} secondes")

@click.group()
def cli():
    pass

editor = VideoEditorCLI()

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def add_video(file_path):
    """Ajoute une vidéo."""
    editor.add_video(file_path)

@cli.command()
@click.argument('video_index', type=int)
@click.argument('start_time', type=str)
@click.argument('end_time', type=str)
def add_segment(video_index, start_time, end_time):
    """Ajoute un segment à une vidéo."""
    editor.add_segment(video_index, start_time, end_time)

@cli.command()
def list_segments():
    """Liste tous les segments."""
    editor.list_segments()

@cli.command()
def list_videos():
    """Liste toutes les vidéos chargées."""
    editor.list_videos()

@cli.command()
@click.argument('order', type=str)
def set_segment_order(order):
    """Définit l'ordre des segments sous forme de paires video_index:segment_index, séparées par des virgules.
       Exemple: "1:1,2:1,1:2" """
    editor.set_segment_order(order)

@cli.command()
@click.argument('output_path', type=click.Path())
def merge_videos(output_path):
    """Fusionne les vidéos et sauvegarde le résultat."""
    editor.merge_videos(output_path)

@cli.command()
def show_stats():
    """Affiche les statistiques des segments et de la vidéo finale."""
    editor.show_stats()

@cli.command()
def interactive():
    """Lance le menu CLI interactif."""
    app = QApplication([])
    while True:
        click.echo("\nMenu:")
        click.echo("1. Ajouter une vidéo")
        click.echo("2. Ajouter un segment")
        click.echo("3. Lister les vidéos")
        click.echo("4. Lister les segments")
        click.echo("5. Définir l'ordre des segments")
        click.echo("6. Fusionner les vidéos")
        click.echo("7. Afficher les statistiques")
        click.echo("8. Quitter")

        choice = click.prompt("Choisissez une option", type=int)

        if choice == 1:
            file_path, _ = QFileDialog.getOpenFileName(None, "Choisissez une vidéo à ajouter", "", "Videos (*.mp4 *.avi *.mov *.mkv)")
            if file_path:
                editor.add_video(file_path)
        elif choice == 2:
            video_index = click.prompt("Entrez l'index de la vidéo", type=int)
            start_time = click.prompt("Entrez le temps de début (en minutes:secondes ou secondes)", type=str)
            end_time = click.prompt("Entrez le temps de fin (en minutes:secondes ou secondes)", type=str)
            editor.add_segment(video_index, start_time, end_time)
        elif choice == 3:
            editor.list_videos()
        elif choice == 4:
            editor.list_segments()
        elif choice == 5:
            click.echo("Entrez l'ordre des segments sous forme de paires video_index:segment_index, séparées par des virgules.")
            click.echo("Exemple: 1:1,2:1,1:2")
            order = click.prompt("Ordre des segments", type=str)
            editor.set_segment_order(order)
        elif choice == 6:
            output_path, _ = QFileDialog.getSaveFileName(None, "Entrez le chemin de sauvegarde de la vidéo fusionnée", "", "Video Files (*.mp4)")
            if output_path:
                editor.merge_videos(output_path)
        elif choice == 7:
            editor.show_stats()
        elif choice == 8:
            break
        else:
            click.echo("Option non valide, veuillez réessayer.")
    app.exit()

if __name__ == '__main__':
    interactive()