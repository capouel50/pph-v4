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

export function toInteger(decimalNumber) {
    // Si la partie fractionnaire du nombre est égale à zéro
    if(decimalNumber % 1 === 0) {

        // Convertir en entier en utilisant le convertisseur Number entier
        return Number.parseInt(decimalNumber, 10);
    }

    // Sinon, retourner le nombre tel quel
    return decimalNumber;
}

export function formatDate(date) {
  var dd = String(date.getDate()).padStart(2, '0');
  var mm = String(date.getMonth() + 1).padStart(2, '0'); // Les mois de l'objet Date commencent à 0, donc ajoutez 1.
  var yyyy = date.getFullYear();

  return dd + '/' + mm + '/' + yyyy;
}