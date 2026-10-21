import React from 'react';

export const StatusBadge = ({ status }) => {
  if (!status) return null;

  const s = status.toLowerCase();

  let styles = 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300';

  if (s.includes('available') || s.includes('completed') || s.includes('paid')) {
    styles = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';
  } else if (s.includes('pending') || s.includes('requested') || s.includes('reserved') || s.includes('unpaid')) {
    styles = 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border-amber-200 dark:border-amber-800';
  } else if (s.includes('sold') || s.includes('recycled') || s.includes('donated')) {
    styles = 'bg-indigo-100 text-indigo-800 dark:bg-indigo-950/60 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800';
  } else if (s.includes('cancelled') || s.includes('failed') || s.includes('damaged') || s.includes('poor')) {
    styles = 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 border-rose-200 dark:border-rose-800';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${styles}`}>
      {status}
    </span>
  );
};
