import matplotlib.pyplot as plt

def main():
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 17. PRIMARY FIGURE SPECIFICATION
    # FEVER B3 AUROC vs AVeriTeC B3 AUROC
    fig, ax = plt.subplots(figsize=(6, 8))
    
    datasets = ['FEVER', 'AVeriTeC']
    auroc = [0.5463, 0.3545]
    colors = ['#1f77b4', '#d62728']
    
    x_pos = np.arange(len(datasets))
    
    bars = ax.bar(x_pos, auroc, color=colors, width=0.5)
    
    # Add chance line
    ax.axhline(y=0.5, color='gray', linestyle='--', label='Chance (0.5)')
    
    # Formatting
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel('B3 AUROC')
    ax.set_title('Cross-Construction Generalization of Density Signal')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([
        'FEVER\n(missing_evidence)', 
        'AVeriTeC\n(retrieved_insufficient)'
    ])
    
    # Add text labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold')
                    
    ax.legend()
    plt.tight_layout()
    plt.savefig('results/FINAL_RESEARCH_FREEZE/figures/fig1_cross_construction.png', dpi=300)
    plt.close()
    
    # 18. SECOND FIGURE - CONSTRUCTION EFFECT
    fig, ax = plt.subplots(figsize=(8, 6))
    
    constructions = ['retrieved_insufficient', 'contradictory', 'rare_valid']
    auroc_const = [0.2754, 0.4273, 0.4637]
    
    y_pos = np.arange(len(constructions))
    
    bars = ax.barh(y_pos, auroc_const, color=['#d62728', '#ff7f0e', '#2ca02c'], height=0.5)
    
    ax.axvline(x=0.5, color='gray', linestyle='--', label='Chance (0.5)')
    
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel('AUROC vs Opposing Class')
    ax.set_title('POST-HOC CONSTRUCTION ANALYSIS (AVeriTeC)')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(constructions)
    
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:.4f}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center', fontweight='bold')
                    
    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('results/FINAL_RESEARCH_FREEZE/figures/fig2_construction_effect.png', dpi=300)
    plt.close()
    
if __name__ == '__main__':
    main()
