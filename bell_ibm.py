# Installation requise: pip install qiskit qiskit-ibm-runtime

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# 1. Configuration - Remplacez par votre token IBM Quantum
# Obtenez votre token sur: https://quantum.ibm.com/
TOKEN = "z5YOGZM1HHwUc4QRdRarvmIKgIvmCIRdLofsRFNc6rIA"

# Sauvegarde du token (à faire une seule fois)
QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=TOKEN, overwrite=True)

# Connexion au service
service = QiskitRuntimeService(channel="ibm_quantum_platform")

# 2. Création d'un circuit quantique simple (Bell State)
qc = QuantumCircuit(2, 2)  # 2 qubits, 2 bits classiques

# Application des portes quantiques
qc.h(0)        # Porte Hadamard sur qubit 0 (superposition)
qc.cx(0, 1)    # Porte CNOT (intrication)
qc.measure([0, 1], [0, 1])  # Mesure des qubits

print("Circuit quantique créé:")
print(qc.draw())

# 3. Exécution sur un VRAI ordinateur quantique !
print("\n--- Test avec ordinateur quantique réel ---")

# Liste les backends disponibles
print("Backends disponibles:")
backends = service.backends()
for backend in backends:
    print(f"  - {backend.name}")

# Sélectionne le moins occupé
backend = service.least_busy(operational=True)
print(f"\nBackend utilisé: {backend.name}")

# IMPORTANT: Transpiler le circuit pour le backend spécifique
print("Transpilation du circuit pour l'architecture quantique...")
qc_transpiled = transpile(qc, backend=backend, optimization_level=3)
print("✓ Circuit transpilé")

sampler = Sampler(backend)
print(f"Soumission du job sur {backend.name}...")
job = sampler.run([qc_transpiled], shots=100)  # 100 mesures pour économiser vos crédits
print(f"Job ID: {job.job_id()}")
print("Attendez... (cela peut prendre quelques secondes ou minutes)")

result = job.result()

# Récupération des résultats
pub_result = result[0]
counts = pub_result.data.c.get_counts()  # 'c' est le nom du registre classique

print(f"\nRésultats: {counts}")
print("\n🎯 Résultats attendus pour un Bell State:")
print("   ~50% de |00⟩ et ~50% de |11⟩ (intrication quantique)")
print("\n⚠️  Note: Sur un vrai ordinateur quantique, vous verrez aussi")
print("   quelques |01⟩ et |10⟩ à cause du bruit quantique!")

print(f"\n✓ Test réussi! Vous avez exécuté votre circuit sur {backend.name}")
print(f"   C'est un VRAI ordinateur quantique IBM! 🚀")