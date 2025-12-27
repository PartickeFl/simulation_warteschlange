import matplotlib
import matplotlib.pyplot as plt
from typing import List, Optional

matplotlib.use("Agg")

class CurveFamily:
    """
    Verwaltet und speichert mehrere Kurven in einem Diagramm.
    Erwartet Listen von Listen:
    x = [[x11, x12, ...], [x21, x22, ...], ...]
    y = [[y11, y12, ...], [y21, y22, ...], ...]
    Jedes (x[i], y[i])-Paar wird als eine Kurve geplottet.
    """

    def __init__(self, x_lists: List[List[float]], y_lists: List[List[float]]) -> None:
        """
        Initialisiert die CurveFamily mit x- und y-Werten für mehrere Kurven.
        :param x_lists: Liste von x-Wert-Listen für jede Kurve
        :param y_lists: Liste von y-Wert-Listen für jede Kurve
        :raises ValueError: Wenn die Anzahl der Kurven in x und y nicht übereinstimmt
        """
        if len(x_lists) != len(y_lists):
            raise ValueError("x and y must contain the same number of curves")

        self.x: List[List[float]] = x_lists
        self.y: List[List[float]] = y_lists

    def save(
        self,
        title: str = "Curve Family",
        x_label: str = "x",
        y_label: str = "y",
        curve_titles: Optional[List[str]] = None,
        show_legend: bool = True,
        linewidth: int = 2,
        filename: str = "curve_family.png"
    ) -> None:
        """
        Speichert das Diagramm mit den Kurven als PNG-Datei.
        :param title: Titel des Diagramms
        :param x_label: Beschriftung der x-Achse
        :param y_label: Beschriftung der y-Achse
        :param curve_titles: Optionale Liste von Kurventiteln
        :param show_legend: Legende anzeigen
        :param linewidth: Liniendicke der Kurven
        :param filename: Dateiname für das gespeicherte Bild
        :raises ValueError: Bei inkonsistenter Kurvenanzahl oder Kurvenlänge
        """
        plt.figure(figsize=(8, 5))

        if curve_titles is not None and len(curve_titles) != len(self.x):
            raise ValueError("curve_titles must have the same length as the number of curves")

        for i, (x_vals, y_vals) in enumerate(zip(self.x, self.y)):
            if len(x_vals) != len(y_vals):
                raise ValueError(f"Curve {i}: x and y must have the same length")

            plt.plot(
                x_vals,
                y_vals,
                label=(curve_titles[i] if curve_titles is not None else f"Curve {i + 1}"),
                linewidth=linewidth
            )

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True, alpha=0.3)

        if show_legend:
            plt.legend()

        plt.tight_layout()
        plt.savefig(filename)

# Beispiel für die Nutzung:
# x = [[0, 1, 2, 3], [0, 1, 2, 3]]
# y = [[0, 1, 4, 9], [0, 1, 2, 3]]
# curves = CurveFamily(x, y)
# curves.save(title="Example Curve Family")
