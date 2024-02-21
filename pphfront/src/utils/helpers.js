export function getCalculatedQty(formula, params, qte, unitMeasureString) {
  for(let param of params){
    let searchTerm = param.parametre.nom + " - " + param.parametre.unite;
    formula = formula.replace(new RegExp(searchTerm, 'g'), param.valeur_parametre);
    let qteSearchTerm = "Quantité - " + unitMeasureString;
    formula = formula.replace(new RegExp(qteSearchTerm, 'g'), qte);
  }
  try {
    let result = eval(formula);
    // Si le résultat est un nombre, le formater avec 3 chiffres après la virgule
    if(!isNaN(result)) {
      return Number(result).toFixed(2);
    } else {
      return result;
    }
  } catch(e) {
    return "Erreur";
  }
}