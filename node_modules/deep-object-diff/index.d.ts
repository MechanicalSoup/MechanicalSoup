export function diff (originalObj: object, updatedObj: object): object

export function addedDiff (originalObj: object, updatedObj: object): object

export function deletedDiff (originalObj: object, updatedObj: object): object

export function updatedDiff (originalObj: object, updatedObj: object): object

export interface DetailedDiff {
    added: object
    deleted: object
    updated: object
}

export function detailedDiff (originalObj: object, updatedObj: object): DetailedDiff
