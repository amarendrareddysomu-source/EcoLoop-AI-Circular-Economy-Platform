"""
ML Algorithm 4: K-Nearest Neighbors (k-NN) Distance Algorithm
File: ai_engine/ml_models/knn_model.py

Implements Non-Parametric Distance-Based Machine Learning using Euclidean metric:
  d(p, q) = sqrt( sum( (p_i - q_i)^2 ) )
Finds k-Nearest Neighbors for item classification and facility cluster matching.
"""

from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

class KNearestNeighborsAlgorithm:
    """
    K-Nearest Neighbors (k-NN) Machine Learning Algorithm wrapper.
    """

    def __init__(self, k_neighbors: int = 5):
        self.k = k_neighbors
        self.knn_classifier = KNeighborsClassifier(n_neighbors=self.k, metric="minkowski", p=2)
        self.nn_search = NearestNeighbors(n_neighbors=self.k, metric="euclidean")
        self.is_trained = False
        self._bootstrap_train()

    def _bootstrap_train(self):
        """
        Populates k-NN dataset with circular economy item vectors.
        Vector: [weight_kg, volume_m3, repairability_score, eco_points]
        """
        X, y = [], []
        # Categories: 0: Electronics, 1: Furniture, 2: Apparel, 3: Scrap Metal, 4: Packaging
        np.random.seed(42)
        for _ in range(80):
            # Electronics
            X.append([np.random.uniform(0.5, 5.0), np.random.uniform(0.01, 0.1), np.random.uniform(70, 95), np.random.uniform(80, 100)])
            y.append(0)
            # Furniture
            X.append([np.random.uniform(10.0, 40.0), np.random.uniform(0.2, 1.5), np.random.uniform(50, 75), np.random.uniform(60, 85)])
            y.append(1)
            # Apparel
            X.append([np.random.uniform(0.2, 2.0), np.random.uniform(0.005, 0.05), np.random.uniform(60, 85), np.random.uniform(70, 90)])
            y.append(2)
            # Scrap Metal
            X.append([np.random.uniform(5.0, 50.0), np.random.uniform(0.05, 0.5), np.random.uniform(10, 35), np.random.uniform(40, 65)])
            y.append(3)
            # Packaging
            X.append([np.random.uniform(0.1, 1.0), np.random.uniform(0.01, 0.2), np.random.uniform(5, 20), np.random.uniform(20, 50)])
            y.append(4)

        X_arr = np.array(X)
        self.knn_classifier.fit(X_arr, y)
        self.nn_search.fit(X_arr)
        self.is_trained = True

    def find_k_nearest(
        self,
        weight_kg: float,
        volume_m3: float,
        repairability_score: float,
        eco_points: float = 75.0,
        k: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Finds k nearest neighbors for an input item vector.
        """
        k_val = k or self.k
        query_vector = np.array([[weight_kg, volume_m3, repairability_score, eco_points]])

        # 1. k-NN Classification Prediction
        predicted_class_idx = int(self.knn_classifier.predict(query_vector)[0])
        class_labels = ["Electronics", "Furniture", "Apparel & Shoes", "Scrap Metal", "Packaging Waste"]
        predicted_category = class_labels[predicted_class_idx]

        # 2. Nearest Neighbors Distance Retrieval
        distances, indices = self.nn_search.kneighbors(query_vector, n_neighbors=k_val)

        neighbors_list = []
        for dist, idx in zip(distances[0], indices[0]):
            neighbors_list.append({
                "neighbor_index": int(idx),
                "euclidean_distance": round(float(dist), 4),
                "similarity_score": round(1.0 / (1.0 + float(dist)), 4)
            })

        return {
            "algorithm_name": "K-Nearest Neighbors (k-NN) Distance Algorithm",
            "k_neighbors_count": k_val,
            "distance_metric": "Minkowski / Euclidean (p=2)",
            "predicted_category_cluster": predicted_category,
            "nearest_neighbors": neighbors_list,
            "closest_neighbor_distance": round(float(distances[0][0]), 4)
        }

knn_algorithm = KNearestNeighborsAlgorithm()
