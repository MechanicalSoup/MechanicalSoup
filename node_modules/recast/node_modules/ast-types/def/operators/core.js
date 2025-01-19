"use strict";;
Object.defineProperty(exports, "__esModule", { value: true });
function default_1() {
    return {
        BinaryOperators: [
            "==", "!=", "===", "!==",
            "<", "<=", ">", ">=",
            "<<", ">>", ">>>",
            "+", "-", "*", "/", "%",
            "&",
            "|", "^", "in",
            "instanceof",
        ],
        AssignmentOperators: [
            "=", "+=", "-=", "*=", "/=", "%=",
            "<<=", ">>=", ">>>=",
            "|=", "^=", "&=",
        ],
        LogicalOperators: [
            "||", "&&",
        ],
    };
}
exports.default = default_1;
module.exports = exports["default"];
